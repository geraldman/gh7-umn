"""Seed the three demo scenarios (ARCHITECTURE.md §5). Idempotent — wipes and
re-inserts. NO LITERAL DATES: everything is relative to date.today() at seed
time, so re-running an hour before the demo guarantees fresh scenarios.

    python -m data.seed

Scenarios (each on its own crop|province price series so they can't interfere):
  oversupply — cabai_merah @ garut (jawa_barat, falling):  4 reports in window → sell + match
  scarcity   — bawang_merah @ brebes (jawa_tengah, rising): 0 other reports    → wait
  neutral    — bawang_merah @ cianjur (jawa_barat, flat):   1 other report     → hold
"""
from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

from core import db
from core.rules import get_recommendation
from data import loader, sources

FALLING = [50000, 49000, 48000, 47000, 44000, 43000, 42000]  # ≈ -11% → falling
RISING = [42000, 43000, 44000, 47000, 48000, 49000, 50000]  # ≈ +11% → rising
FLAT = [45000, 45200, 44800, 45000, 45100, 44900, 45000]  # ≈  0% → flat


def _series(prices: list[int], today: date) -> list[dict]:
    """7 data days ending yesterday."""
    start = today - timedelta(days=len(prices))
    return [
        {"date": (start + timedelta(days=i)).isoformat(), "price_idr_per_kg": p}
        for i, p in enumerate(prices)
    ]


def seed(
    dsn: str | None = None,
    cache_path: str | Path | None = None,
    today: date | None = None,
):
    today = today or date.today()
    conn = db.get_connection(dsn)
    db.wipe_db(conn)

    # --- Farmers -------------------------------------------------------------
    farmers = [
        # (telegram_id, name, region) — farmer 6 is the live-demo reporter
        ("tg-1001", "Pak Asep", "garut"),
        ("tg-1002", "Bu Imas", "garut"),
        ("tg-1003", "Pak Dedi", "garut"),
        ("tg-1004", "Pak Ujang", "garut"),
        ("tg-1005", "Bu Euis", "cianjur"),
        ("tg-9999", "Demo Farmer", "garut"),
    ]
    for tg, name, region in farmers:
        conn.execute(
            "INSERT INTO farmer (telegram_id, name, region) VALUES (%s, %s, %s)",
            (tg, name, region),
        )

    # --- Harvest reports (relative dates) -------------------------------------
    d = lambda offset: (today + timedelta(days=offset)).isoformat()
    reports = [
        # oversupply cluster: 4 reports within ±2 days of today+2
        (1, "cabai_merah", "garut", d(1), 120),
        (2, "cabai_merah", "garut", d(2), 150),
        (3, "cabai_merah", "garut", d(2), 100),
        (4, "cabai_merah", "garut", d(3), 200),
        # neutral: exactly one existing report (new one makes 2 < 3, not crowded)
        (5, "bawang_merah", "cianjur", d(2), 80),
        # scarcity (brebes): deliberately no reports
    ]
    for r in reports:
        conn.execute(
            "INSERT INTO harvest_report (farmer_id, crop, region, harvest_date,"
            " quantity_kg) VALUES (%s, %s, %s, %s, %s)",
            r,
        )
    conn.commit()

    # --- Price series → cache JSON + snapshot table ---------------------------
    # Start from the existing cache so imported real series (scripts/
    # import_bi_csv.py) survive a reseed; the three scenario keys below are
    # merged on top and stay authoritative for their date range.
    cache = loader.load_cache(cache_path)
    loader.merge_rows(cache, "cabai_merah", "jawa_barat", _series(FALLING, today))
    loader.merge_rows(cache, "bawang_merah", "jawa_tengah", _series(RISING, today))
    loader.merge_rows(cache, "bawang_merah", "jawa_barat", _series(FLAT, today))
    loader.save_cache(cache, cache_path)
    loader.sync_snapshots_table(conn, cache)
    return conn


def verify(conn, cache_path=None, today: date | None = None) -> list[tuple]:
    """Run the three scenarios read-only and return (name, expected, result)."""
    chain = sources.ChainedSource([sources.CachedSource(cache_path)])
    kw = dict(conn=conn, chain=chain, today=today)
    return [
        ("oversupply", "sell", get_recommendation("cabai_merah", "garut", 2, **kw)),
        ("scarcity", "wait", get_recommendation("bawang_merah", "brebes", 2, **kw)),
        ("neutral", "hold", get_recommendation("bawang_merah", "cianjur", 2, **kw)),
    ]


if __name__ == "__main__":
    conn = seed()
    print("Seeded. Verifying scenarios:\n")
    ok = True
    for name, expected, result in verify(conn):
        got = result["recommendation"]
        mark = "OK " if got == expected else "FAIL"
        ok &= got == expected
        print(f"  [{mark}] {name:<10} expected={expected:<4} got={got:<4}")
        print(f"         {result['reason']}")
    print("\nAll scenarios correct." if ok else "\nSCENARIO MISMATCH — check seeds.")
