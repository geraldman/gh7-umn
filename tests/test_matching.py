"""Tests for plan_fill() — Earliest-Deadline-First buy allocation."""
from __future__ import annotations

from core.matching import plan_fill


def _r(id, remaining, date):
    return {"id": id, "remaining_kg": remaining, "harvest_date": date}


def test_fills_earliest_harvest_first_and_combines():
    # buyer wants 200: take all 90 from the day-1 farmer, then 110 from day-2.
    reports = [_r(1, 200, "2026-07-19"), _r(2, 90, "2026-07-18")]
    allocs, short = plan_fill(reports, 200)
    assert short == 0
    assert [(a["report"]["id"], a["take_kg"]) for a in allocs] == [(2, 90), (1, 110)]


def test_shortfall_when_not_enough_stock():
    allocs, short = plan_fill([_r(1, 50, "2026-07-18")], 200)
    assert short == 150
    assert allocs[0]["take_kg"] == 50


def test_exact_single_report():
    allocs, short = plan_fill([_r(1, 200, "2026-07-18")], 200)
    assert short == 0
    assert len(allocs) == 1 and allocs[0]["take_kg"] == 200


def test_stops_once_filled_and_skips_later_farmers():
    reports = [_r(1, 300, "2026-07-18"), _r(2, 300, "2026-07-19")]
    allocs, short = plan_fill(reports, 100)
    assert short == 0
    assert len(allocs) == 1 and allocs[0]["report"]["id"] == 1


def test_skips_zero_remaining():
    reports = [_r(1, 0, "2026-07-18"), _r(2, 80, "2026-07-19")]
    allocs, short = plan_fill(reports, 80)
    assert short == 0
    assert [a["report"]["id"] for a in allocs] == [2]
