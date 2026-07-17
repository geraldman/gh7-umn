"""Adapter-side storage: Telegram role registry + read/update views over the
core tables. All *writes* of harvest reports and matches go through
core.api.process_harvest_report — this module never inserts those itself
(ARCHITECTURE.md §6).
"""
from __future__ import annotations

import psycopg

from core import db

# The role table is bot-local state (who pressed which role button); it lives
# in the same database for convenience but is owned by the adapter.
_ROLE_SCHEMA = """
CREATE TABLE IF NOT EXISTS bot_role (
    user_id  BIGINT PRIMARY KEY,
    username TEXT,
    role     TEXT NOT NULL CHECK (role IN ('Farmer','Buyer','Coordinator'))
);
"""

_conn: psycopg.Connection | None = None


def get_connection() -> psycopg.Connection:
    """One long-lived connection for the (single-threaded) bot, re-opened if
    the network dropped it. rollback() on checkout clears any transaction a
    failed handler left open, so one error can't poison later handlers."""
    global _conn
    if _conn is not None:
        try:
            _conn.rollback()          # clear any tx a failed handler left open
            _conn.execute("SELECT 1")  # real round trip: detects dropped conns
            _conn.rollback()
            return _conn
        except psycopg.Error:
            try:
                _conn.close()
            except psycopg.Error:
                pass
            _conn = None
    _conn = db.get_connection()
    _conn.execute(_ROLE_SCHEMA)
    # Buyer's operating region (nullable; older deployments predate the column).
    _conn.execute("ALTER TABLE bot_role ADD COLUMN IF NOT EXISTS region TEXT")
    _conn.commit()
    return _conn


# --- Roles -------------------------------------------------------------------

def set_user_role(conn, user_id: int, username: str | None, role: str) -> None:
    conn.execute(
        "INSERT INTO bot_role (user_id, username, role) VALUES (%s, %s, %s)"
        " ON CONFLICT(user_id) DO UPDATE SET username = excluded.username,"
        " role = excluded.role",
        (user_id, username, role),
    )
    conn.commit()


def get_user_role(conn, user_id: int) -> str | None:
    row = conn.execute(
        "SELECT role FROM bot_role WHERE user_id = %s", (user_id,)
    ).fetchone()
    return row["role"] if row else None


def get_users_by_role(conn, role: str) -> list[dict]:
    return conn.execute(
        "SELECT user_id, username FROM bot_role WHERE role = %s", (role,)
    ).fetchall()


def get_all_users(conn) -> list[dict]:
    """Every registered user, any role — the /admin broadcast audience."""
    return conn.execute("SELECT user_id, username, role FROM bot_role").fetchall()


def set_user_region(conn, user_id: int, region: str) -> None:
    conn.execute(
        "UPDATE bot_role SET region = %s WHERE user_id = %s", (region, user_id)
    )
    conn.commit()


def get_user_region(conn, user_id: int) -> str | None:
    row = conn.execute(
        "SELECT region FROM bot_role WHERE user_id = %s", (user_id,)
    ).fetchone()
    return row["region"] if row else None


# --- Farmer mapping (telegram user -> core farmer row) --------------------------

def get_or_create_farmer(
    conn, telegram_id: int, name: str | None, region: str, phone: str | None = None
) -> int:
    row = conn.execute(
        "SELECT id FROM farmer WHERE telegram_id = %s", (str(telegram_id),)
    ).fetchone()
    if row:
        conn.execute(
            "UPDATE farmer SET region = %s, name = COALESCE(%s, name),"
            " phone = COALESCE(%s, phone) WHERE id = %s",
            (region, name, phone, row["id"]),
        )
        conn.commit()
        return row["id"]
    farmer_id = conn.execute(
        "INSERT INTO farmer (telegram_id, name, region, phone)"
        " VALUES (%s, %s, %s, %s) RETURNING id",
        (str(telegram_id), name, region, phone),
    ).fetchone()["id"]
    conn.commit()
    return farmer_id


# --- Match views / status updates (statuses match the core schema:
#     pending | confirmed | declined) ------------------------------------------

def get_match(conn, match_id: int | str):
    # int() — callback data arrives as a string; Postgres won't compare
    # integer columns to text params (SQLite silently did).
    return conn.execute(
        "SELECT mr.id, mr.status, mr.harvest_report_id,"
        "       hr.crop, hr.region, hr.harvest_date, hr.quantity_kg,"
        "       f.telegram_id AS farmer_telegram_id, f.name AS farmer_name,"
        "       f.phone AS farmer_phone"
        " FROM match_request mr"
        " JOIN harvest_report hr ON hr.id = mr.harvest_report_id"
        " JOIN farmer f ON f.id = hr.farmer_id"
        " WHERE mr.id = %s",
        (int(match_id),),
    ).fetchone()


def update_match_status(conn, match_id: int | str, status: str) -> None:
    assert status in ("pending", "confirmed", "declined")
    conn.execute(
        "UPDATE match_request SET status = %s WHERE id = %s",
        (status, int(match_id)),
    )
    conn.commit()


def get_reports_by_region(conn, region: str) -> list[dict]:
    return conn.execute(
        "SELECT hr.crop, hr.harvest_date, hr.quantity_kg, f.name AS farmer_name"
        " FROM harvest_report hr"
        " JOIN farmer f ON f.id = hr.farmer_id"
        " WHERE hr.region = %s"
        " ORDER BY hr.crop, hr.harvest_date",
        (region,),
    ).fetchall()


def get_all_matches(conn) -> list[dict]:
    return conn.execute(
        "SELECT mr.id, mr.status, hr.crop, hr.region, hr.harvest_date,"
        "       hr.quantity_kg, f.name AS farmer_name"
        " FROM match_request mr"
        " JOIN harvest_report hr ON hr.id = mr.harvest_report_id"
        " JOIN farmer f ON f.id = hr.farmer_id"
        " ORDER BY mr.created_at DESC",
    ).fetchall()
