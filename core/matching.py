"""Buyer-match creation (ARCHITECTURE.md §4): when the recommendation is
"sell", create a pending MatchRequest for the anchor buyer."""
from __future__ import annotations

import psycopg

ANCHOR_BUYER_ID = 1


def plan_fill(reports: list[dict], target_kg: float) -> tuple[list[dict], float]:
    """Earliest-Deadline-First allocation of a buyer's target across farmers.

    Perishables spoil on their harvest_date, so we fill from the earliest
    harvest first — the crop with the least time left gets sold first,
    minimising spoilage. Partial fills are allowed (split one farmer's stock).

    `reports`: dicts with at least `remaining_kg` and `harvest_date`.
    Returns (allocations, shortfall): allocations = [{"report": r,
    "take_kg": n}], shortfall = kg still unmet (0 if fully filled).
    """
    need = target_kg
    allocations: list[dict] = []
    for r in sorted(reports, key=lambda r: r["harvest_date"]):
        if need <= 0:
            break
        avail = r["remaining_kg"]
        if avail <= 0:
            continue
        take = min(avail, need)
        allocations.append({"report": r, "take_kg": take})
        need -= take
    return allocations, max(0.0, need)


def create_match_request(
    conn: psycopg.Connection, harvest_report_id: int, buyer_id: int = ANCHOR_BUYER_ID
) -> int | None:
    """Create a pending MatchRequest. Returns its id, or None if a pending
    match already exists for this report (the double-sell guard)."""
    existing = conn.execute(
        "SELECT id FROM match_request"
        " WHERE harvest_report_id = %s AND status = 'pending'",
        (harvest_report_id,),
    ).fetchone()
    if existing:
        return None
    match_id = conn.execute(
        "INSERT INTO match_request (harvest_report_id, buyer_id)"
        " VALUES (%s, %s) RETURNING id",
        (harvest_report_id, buyer_id),
    ).fetchone()["id"]
    conn.commit()
    return match_id
