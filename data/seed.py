"""Seed the demo scenarios (ARCHITECTURE.md §5). Idempotent — wipes and
re-inserts. NO LITERAL DATES: harvest reports are relative to date.today() at
seed time, so re-running an hour before the demo guarantees fresh scenarios.

    python -m data.seed

Prices are REAL Bank Indonesia data (Cabai Rawit Merah), imported from the
CSVs in uploads/. The current market is flat, so the scenarios are driven by
the harvest-cluster signal — which is exactly the point of the product:

  oversupply — cabai_rawit_merah @ garut  (4 reports in window): flat market
               but a local glut is forming → sell + buyer match
  neutral    — cabai_rawit_merah @ cianjur (1 report):           flat, no glut → hold

The "wait" case (rising price, no glut) needs a rising series; no real series
is rising this week, so it's covered by the unit tests, not the live seed.
"""
from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

from core import db
from core.rules import get_recommendation
from data import loader, sources
from scripts.import_bi_csv import import_dir

UPLOADS_DIR = Path(__file__).resolve().parent.parent / "uploads"


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
        (1, "cabai_rawit_merah", "garut", d(1), 120),
        (2, "cabai_rawit_merah", "garut", d(2), 150),
        (3, "cabai_rawit_merah", "garut", d(2), 100),
        (4, "cabai_rawit_merah", "garut", d(3), 200),
        # neutral: exactly one existing report (new one makes 2 < 3, not crowded)
        (5, "cabai_rawit_merah", "cianjur", d(2), 80),
    ]
    for r in reports:
        conn.execute(
            "INSERT INTO harvest_report (farmer_id, crop, region, harvest_date,"
            " quantity_kg) VALUES (%s, %s, %s, %s, %s)",
            r,
        )
    conn.commit()

    # --- Price series: real Bank Indonesia data -------------------------------
    # Import the scraped BI CSVs (idempotent, local files — no network) so the
    # demo reads real cabai_rawit_merah prices, then mirror into the snapshot
    # table. If uploads/ is absent, fall back to whatever's already cached.
    if UPLOADS_DIR.exists():
        import_dir(UPLOADS_DIR, cache_path)
    cache = loader.load_cache(cache_path)
    loader.sync_snapshots_table(conn, cache)
    return conn


def verify(conn, cache_path=None, today: date | None = None) -> list[tuple]:
    """Run the three scenarios read-only and return (name, expected, result)."""
    chain = sources.ChainedSource([sources.CachedSource(cache_path)])
    kw = dict(conn=conn, chain=chain, today=today)
    return [
        ("oversupply", "sell", get_recommendation("cabai_rawit_merah", "garut", 2, **kw)),
        ("neutral", "hold", get_recommendation("cabai_rawit_merah", "cianjur", 2, **kw)),
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
