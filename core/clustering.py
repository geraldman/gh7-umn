"""Cluster detection: how many harvest reports land on the same local market
at the same time (ARCHITECTURE.md §4).

The window slides per report: ±2 days around the queried harvest date, same
crop, same *district*. It is not a fixed calendar bucket — two farmers five
days apart are simply not in each other's cluster.
"""
from __future__ import annotations

import sqlite3
from datetime import date, timedelta

WINDOW_DAYS = 2


def count_cluster(
    conn: sqlite3.Connection, crop: str, region: str, harvest_date: date
) -> int:
    """Count reports for crop+district within ±WINDOW_DAYS of harvest_date.

    Call this *after* inserting the new report: the count includes it, and the
    crowded threshold in the rule engine is defined as "≥3 including this one".
    """
    lo = (harvest_date - timedelta(days=WINDOW_DAYS)).isoformat()
    hi = (harvest_date + timedelta(days=WINDOW_DAYS)).isoformat()
    row = conn.execute(
        "SELECT COUNT(*) FROM harvest_report"
        " WHERE crop = ? AND region = ? AND harvest_date BETWEEN ? AND ?",
        (crop, region, lo, hi),
    ).fetchone()
    return row[0]
