"""SQLite connection + schema for Panen Pas (ARCHITECTURE.md §3)."""
from __future__ import annotations

import sqlite3
from pathlib import Path

DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent / "panen.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS farmer (
    id          INTEGER PRIMARY KEY,
    telegram_id TEXT UNIQUE,
    name        TEXT,
    region      TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS harvest_report (
    id           INTEGER PRIMARY KEY,
    farmer_id    INTEGER NOT NULL REFERENCES farmer(id),
    crop         TEXT NOT NULL,
    region       TEXT NOT NULL,
    harvest_date TEXT NOT NULL,
    quantity_kg  REAL,
    created_at   TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS price_snapshot (
    id               INTEGER PRIMARY KEY,
    crop             TEXT NOT NULL,
    region           TEXT NOT NULL,
    date             TEXT NOT NULL,
    price_idr_per_kg INTEGER NOT NULL,
    UNIQUE (crop, region, date)
);

CREATE TABLE IF NOT EXISTS match_request (
    id                INTEGER PRIMARY KEY,
    harvest_report_id INTEGER NOT NULL REFERENCES harvest_report(id),
    buyer_id          INTEGER NOT NULL DEFAULT 1,
    status            TEXT NOT NULL DEFAULT 'pending'
                      CHECK (status IN ('pending','confirmed','declined')),
    created_at        TEXT NOT NULL DEFAULT (datetime('now'))
);
"""

_TABLES = ("match_request", "harvest_report", "price_snapshot", "farmer")


def get_connection(path: str | Path | None = None) -> sqlite3.Connection:
    conn = sqlite3.connect(str(path or DEFAULT_DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA)
    conn.commit()


def wipe_db(conn: sqlite3.Connection) -> None:
    """Delete all rows (keeps schema). Used by the idempotent seeder."""
    init_db(conn)
    for table in _TABLES:  # order respects FK constraints
        conn.execute(f"DELETE FROM {table}")
    conn.commit()
