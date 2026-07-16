"""PostgreSQL connection + schema for Panen Pas (ARCHITECTURE.md §3).

Which database (all read from the repo-root .env or the environment):

    DB_TARGET=local     -> DATABASE_URL_LOCAL    (default: docker compose db)
    DB_TARGET=supabase  -> DATABASE_URL_SUPABASE (the shared team DB)

DATABASE_URL, if set, overrides the toggle entirely (used by containers and
one-off runs). The test suite ignores all of this — see tests/conftest.py.

Dates (harvest_date, price date) are deliberately stored as ISO-8601 TEXT:
they compare/sort correctly as strings, and every reader gets back the same
`str` values it wrote — no date-object surprises across the codebase.
"""
from __future__ import annotations

import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=False)

# The docker-compose local Postgres (offline/demo fallback).
DEFAULT_DSN = "postgresql://postgres:postgres@localhost:5433/panen"

SCHEMA = """
CREATE TABLE IF NOT EXISTS farmer (
    id          INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    telegram_id TEXT UNIQUE,
    name        TEXT,
    region      TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS harvest_report (
    id           INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    farmer_id    INTEGER NOT NULL REFERENCES farmer(id),
    crop         TEXT NOT NULL,
    region       TEXT NOT NULL,
    harvest_date TEXT NOT NULL,
    quantity_kg  DOUBLE PRECISION,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS price_snapshot (
    id               INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    crop             TEXT NOT NULL,
    region           TEXT NOT NULL,
    date             TEXT NOT NULL,
    price_idr_per_kg INTEGER NOT NULL,
    UNIQUE (crop, region, date)
);

CREATE TABLE IF NOT EXISTS match_request (
    id                INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    harvest_report_id INTEGER NOT NULL REFERENCES harvest_report(id),
    buyer_id          INTEGER NOT NULL DEFAULT 1,
    status            TEXT NOT NULL DEFAULT 'pending'
                      CHECK (status IN ('pending','confirmed','declined')),
    created_at        TIMESTAMPTZ NOT NULL DEFAULT now()
);
"""


def resolve_dsn(dsn: str | None = None) -> str:
    """Precedence: explicit arg > DATABASE_URL > DB_TARGET toggle > local."""
    if dsn:
        return str(dsn)
    if os.environ.get("DATABASE_URL"):
        return os.environ["DATABASE_URL"]
    target = os.environ.get("DB_TARGET", "local").strip().lower()
    if target == "supabase":
        url = os.environ.get("DATABASE_URL_SUPABASE")
        if not url:
            raise RuntimeError(
                "DB_TARGET=supabase but DATABASE_URL_SUPABASE is not set in .env"
            )
        return url
    if target != "local":
        raise RuntimeError(f"DB_TARGET must be 'local' or 'supabase', got {target!r}")
    return os.environ.get("DATABASE_URL_LOCAL") or DEFAULT_DSN


def describe_dsn(dsn: str | None = None) -> str:
    """Safe-to-print summary (no password): 'host:port/dbname'."""
    url = resolve_dsn(dsn)
    tail = url.rsplit("@", 1)[-1]
    return tail or url


def get_connection(dsn: str | None = None) -> psycopg.Connection:
    """Rows come back as dicts: row["col"]. Positional row[0] does NOT work —
    alias aggregates (COUNT(*) AS n) and access by name."""
    return psycopg.connect(resolve_dsn(dsn), row_factory=dict_row)


def init_db(conn: psycopg.Connection) -> None:
    conn.execute(SCHEMA)
    conn.commit()


def wipe_db(conn: psycopg.Connection) -> None:
    """Delete all rows and reset id sequences (keeps schema). Used by the
    idempotent seeder — seeds and tests rely on ids starting from 1."""
    init_db(conn)
    conn.execute(
        "TRUNCATE match_request, harvest_report, price_snapshot, farmer"
        " RESTART IDENTITY CASCADE"
    )
    conn.commit()
