"""End-to-end orchestrator tests: the three demo scenarios plus the guards
(ARCHITECTURE.md §2, §5, §7)."""
from __future__ import annotations

from datetime import timedelta

from core.api import process_harvest_report
from tests.conftest import FALLING, FLAT, RISING, TODAY, FakeChain, insert_report, make_series


def _call(conn, chain, farmer_id=1, crop="cabai_rawit_merah", region="garut", days=2, qty=100):
    return process_harvest_report(
        farmer_id, crop, region, days, qty, conn=conn, chain=chain, today=TODAY
    )


def _match_count(conn, status=None):
    q = "SELECT COUNT(*) AS n FROM match_request"
    if status:
        return conn.execute(q + " WHERE status = %s", (status,)).fetchone()["n"]
    return conn.execute(q).fetchone()["n"]


def _report_count(conn):
    return conn.execute("SELECT COUNT(*) AS n FROM harvest_report").fetchone()["n"]


# --- The three seeded demo scenarios ------------------------------------------

def test_oversupply_scenario_sells_and_creates_match(conn):
    hd = TODAY + timedelta(days=2)
    for fid, offset in ((2, -1), (3, 0), (4, 0), (5, 1)):  # 4 neighbors in window
        insert_report(conn, fid, "cabai_rawit_merah", "garut", hd + timedelta(days=offset))
    result = _call(conn, FakeChain(make_series(FALLING)), farmer_id=1)
    assert result["recommendation"] == "sell"
    assert result["match_request_id"] is not None
    assert _match_count(conn, "pending") == 1


def test_scarcity_scenario_waits(conn):
    result = _call(conn, FakeChain(make_series(RISING)))
    assert result["recommendation"] == "wait"
    assert result["match_request_id"] is None
    assert _match_count(conn) == 0


def test_neutral_scenario_holds(conn):
    hd = TODAY + timedelta(days=2)
    insert_report(conn, 2, "cabai_rawit_merah", "garut", hd)  # one neighbor → 2 total
    result = _call(conn, FakeChain(make_series(FLAT)))
    assert result["recommendation"] == "hold"
    assert _match_count(conn) == 0


# --- Validation gate ------------------------------------------------------------

def test_unknown_crop_no_insert_no_match(conn):
    result = _call(conn, FakeChain([]), crop="durian")
    assert result["recommendation"] == "hold"
    assert "durian" in result["reason"]
    assert _report_count(conn) == 0
    assert _match_count(conn) == 0


def test_unknown_region_no_insert_no_match(conn):
    result = _call(conn, FakeChain([]), region="atlantis")
    assert result["recommendation"] == "hold"
    assert _report_count(conn) == 0


# --- Duplicate / double-sell guards ----------------------------------------------

def test_duplicate_report_upserts_not_inserts(conn):
    chain = FakeChain(make_series(FLAT))
    _call(conn, chain, days=2, qty=100)
    _call(conn, chain, days=3, qty=150)  # same farmer+crop+region, in window
    assert _report_count(conn) == 1
    qty = conn.execute("SELECT quantity_kg FROM harvest_report").fetchone()["quantity_kg"]
    assert qty == 150  # updated, not duplicated


def test_sell_twice_creates_only_one_pending_match(conn):
    hd = TODAY + timedelta(days=2)
    for fid, offset in ((2, -1), (3, 0), (4, 1)):
        insert_report(conn, fid, "cabai_rawit_merah", "garut", hd + timedelta(days=offset))
    chain = FakeChain(make_series(FALLING))
    first = _call(conn, chain)
    second = _call(conn, chain)  # farmer retries
    assert first["recommendation"] == second["recommendation"] == "sell"
    assert first["match_request_id"] is not None
    assert second["match_request_id"] is None  # guard fired
    assert _match_count(conn, "pending") == 1


# --- Cluster includes the new report ----------------------------------------------

def test_new_report_completes_the_cluster(conn):
    """Two existing + the new one = 3 = crowded → flat trend flips to sell."""
    hd = TODAY + timedelta(days=2)
    insert_report(conn, 2, "cabai_rawit_merah", "garut", hd)
    insert_report(conn, 3, "cabai_rawit_merah", "garut", hd)
    result = _call(conn, FakeChain(make_series(FLAT)))
    assert result["cluster_size"] == 3
    assert result["recommendation"] == "sell"


# --- Frozen-today injection ---------------------------------------------------------

def test_today_is_injectable_and_deterministic(conn):
    r1 = _call(conn, FakeChain(make_series(FLAT)))
    assert r1["harvest_report_id"] is not None
    hd = conn.execute("SELECT harvest_date FROM harvest_report").fetchone()["harvest_date"]
    assert hd == (TODAY + timedelta(days=2)).isoformat()
