"""The orchestrator — the ONE function Developer B's bot calls, and the single
write path into core tables (ARCHITECTURE.md §2).

Sequence: validate keys → upsert HarvestReport (duplicate guard) →
get_recommendation → on "sell", create pending MatchRequest → return the
contract dict {recommendation, reason, ...}.
"""
from __future__ import annotations

from datetime import date, timedelta

import psycopg

from core import db
from core.clustering import WINDOW_DAYS
from core.matching import create_match_request
from core.models import CROPS, REGION_TO_PROVINCE
from core.rules import get_recommendation


def find_existing_report(
    conn: psycopg.Connection,
    farmer_id: int,
    crop: str,
    region: str,
    days_to_harvest: int,
    today: date | None = None,
):
    """The report the duplicate-guard would update: same farmer+crop+region
    within the cluster window. Returns {id, quantity_kg} or None. Lets the
    adapter ask 'add or replace?' before overwriting an existing quantity."""
    today = today or date.today()
    lo = (today + timedelta(days=days_to_harvest - WINDOW_DAYS)).isoformat()
    hi = (today + timedelta(days=days_to_harvest + WINDOW_DAYS)).isoformat()
    return conn.execute(
        "SELECT id, quantity_kg FROM harvest_report"
        " WHERE farmer_id = %s AND crop = %s AND region = %s"
        " AND harvest_date BETWEEN %s AND %s",
        (farmer_id, crop, region, lo, hi),
    ).fetchone()


def process_harvest_report(
    farmer_id: int,
    crop: str,
    region: str,
    days_to_harvest: int,
    quantity_kg: float | None = None,
    *,
    conn: psycopg.Connection | None = None,
    chain=None,
    today: date | None = None,
) -> dict:
    # 1. Validate at the boundary — unknown key: no insert, no match, honest hold.
    #    LLM/adapter output is untrusted input regardless of which ladder tier
    #    produced it (ARCHITECTURE.md §2).
    if crop not in CROPS:
        return {
            "recommendation": "hold",
            "reason": f"unknown crop '{crop}' — no price data available",
            "match_request_id": None,
        }
    if region not in REGION_TO_PROVINCE:
        return {
            "recommendation": "hold",
            "reason": f"unknown region '{region}' — no data available",
            "match_request_id": None,
        }

    conn = conn if conn is not None else db.get_connection()
    today = today or date.today()
    harvest_date = (today + timedelta(days=days_to_harvest)).isoformat()

    # 2. Duplicate guard: same farmer+crop+region within the cluster window is
    #    an update, not a second report (would self-inflate the cluster count).
    lo = (today + timedelta(days=days_to_harvest - WINDOW_DAYS)).isoformat()
    hi = (today + timedelta(days=days_to_harvest + WINDOW_DAYS)).isoformat()
    existing = conn.execute(
        "SELECT id FROM harvest_report"
        " WHERE farmer_id = %s AND crop = %s AND region = %s"
        " AND harvest_date BETWEEN %s AND %s",
        (farmer_id, crop, region, lo, hi),
    ).fetchone()
    if existing:
        report_id = existing["id"]
        conn.execute(
            "UPDATE harvest_report SET harvest_date = %s, quantity_kg = %s WHERE id = %s",
            (harvest_date, quantity_kg, report_id),
        )
    else:
        report_id = conn.execute(
            "INSERT INTO harvest_report (farmer_id, crop, region, harvest_date,"
            " quantity_kg) VALUES (%s, %s, %s, %s, %s) RETURNING id",
            (farmer_id, crop, region, harvest_date, quantity_kg),
        ).fetchone()["id"]
    conn.commit()

    # 3–4. Signals + rule table (read-only; cluster count now includes this report).
    result = get_recommendation(
        crop, region, days_to_harvest, conn=conn, chain=chain, today=today
    )

    # 5. On "sell", open the buyer channel (guarded against double-creation).
    match_id = None
    if result["recommendation"] == "sell":
        match_id = create_match_request(conn, report_id)
    result["match_request_id"] = match_id
    result["harvest_report_id"] = report_id
    return result
