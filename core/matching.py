"""Buyer-match creation (ARCHITECTURE.md §4): when the recommendation is
"sell", create a pending MatchRequest for the anchor buyer."""
from __future__ import annotations

import sqlite3

ANCHOR_BUYER_ID = 1


def create_match_request(
    conn: sqlite3.Connection, harvest_report_id: int, buyer_id: int = ANCHOR_BUYER_ID
) -> int | None:
    """Create a pending MatchRequest. Returns its id, or None if a pending
    match already exists for this report (the double-sell guard)."""
    existing = conn.execute(
        "SELECT id FROM match_request"
        " WHERE harvest_report_id = ? AND status = 'pending'",
        (harvest_report_id,),
    ).fetchone()
    if existing:
        return None
    cur = conn.execute(
        "INSERT INTO match_request (harvest_report_id, buyer_id) VALUES (?, ?)",
        (harvest_report_id, buyer_id),
    )
    conn.commit()
    return cur.lastrowid
