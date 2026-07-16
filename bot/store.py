"""Adapter-side storage: Telegram role registry + read/update views over the
core tables. All *writes* of harvest reports and matches go through
core.api.process_harvest_report — this module never inserts those itself
(ARCHITECTURE.md §6).
"""
from __future__ import annotations

import sqlite3

from core import db

# The role table is bot-local state (who pressed which role button); it lives
# in the same panen.db for convenience but is owned by the adapter.
_ROLE_SCHEMA = """
CREATE TABLE IF NOT EXISTS bot_role (
    user_id  INTEGER PRIMARY KEY,
    username TEXT,
    role     TEXT NOT NULL CHECK (role IN ('Farmer','Buyer','Coordinator'))
);
"""


def get_connection() -> sqlite3.Connection:
    conn = db.get_connection()
    conn.executescript(_ROLE_SCHEMA)
    return conn


# --- Roles -------------------------------------------------------------------

def set_user_role(conn, user_id: int, username: str | None, role: str) -> None:
    conn.execute(
        "INSERT INTO bot_role (user_id, username, role) VALUES (?, ?, ?)"
        " ON CONFLICT(user_id) DO UPDATE SET username = excluded.username,"
        " role = excluded.role",
        (user_id, username, role),
    )
    conn.commit()


def get_user_role(conn, user_id: int) -> str | None:
    row = conn.execute(
        "SELECT role FROM bot_role WHERE user_id = ?", (user_id,)
    ).fetchone()
    return row["role"] if row else None


def get_users_by_role(conn, role: str) -> list[sqlite3.Row]:
    return conn.execute(
        "SELECT user_id, username FROM bot_role WHERE role = ?", (role,)
    ).fetchall()


# --- Farmer mapping (telegram user -> core farmer row) --------------------------

def get_or_create_farmer(conn, telegram_id: int, name: str | None, region: str) -> int:
    row = conn.execute(
        "SELECT id FROM farmer WHERE telegram_id = ?", (str(telegram_id),)
    ).fetchone()
    if row:
        conn.execute(
            "UPDATE farmer SET region = ?, name = COALESCE(?, name) WHERE id = ?",
            (region, name, row["id"]),
        )
        conn.commit()
        return row["id"]
    cur = conn.execute(
        "INSERT INTO farmer (telegram_id, name, region) VALUES (?, ?, ?)",
        (str(telegram_id), name, region),
    )
    conn.commit()
    return cur.lastrowid


# --- Match views / status updates (statuses match the core schema:
#     pending | confirmed | declined) ------------------------------------------

def get_match(conn, match_id: int | str):
    return conn.execute(
        "SELECT mr.id, mr.status, mr.harvest_report_id,"
        "       hr.crop, hr.region, hr.harvest_date, hr.quantity_kg,"
        "       f.telegram_id AS farmer_telegram_id, f.name AS farmer_name"
        " FROM match_request mr"
        " JOIN harvest_report hr ON hr.id = mr.harvest_report_id"
        " JOIN farmer f ON f.id = hr.farmer_id"
        " WHERE mr.id = ?",
        (match_id,),
    ).fetchone()


def update_match_status(conn, match_id: int | str, status: str) -> None:
    assert status in ("pending", "confirmed", "declined")
    conn.execute(
        "UPDATE match_request SET status = ? WHERE id = ?", (status, match_id)
    )
    conn.commit()


def get_all_matches(conn) -> list[sqlite3.Row]:
    return conn.execute(
        "SELECT mr.id, mr.status, hr.crop, hr.region, hr.harvest_date,"
        "       hr.quantity_kg, f.name AS farmer_name"
        " FROM match_request mr"
        " JOIN harvest_report hr ON hr.id = mr.harvest_report_id"
        " JOIN farmer f ON f.id = hr.farmer_id"
        " ORDER BY mr.created_at DESC",
    ).fetchall()
