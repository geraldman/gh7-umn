"""Price cache I/O (ARCHITECTURE.md §4).

data/price_cache.json is the source of truth for price history; the
price_snapshot table is just its queryable form. Cache shape:

    { "<crop>|<province>": [ {"date": "2026-07-10", "price_idr_per_kg": 42000}, ... ] }

TODO(live-sources): when PIHPS/PanelHarga XHR capture lands, keys grow a
per-source suffix ("crop|province|source") internally and flatten for the
terminal cache fallback — see §4 chain rules.
"""
from __future__ import annotations

import json
from pathlib import Path
from statistics import mean, pstdev

import psycopg

from core.models import PriceSnapshot

DEFAULT_CACHE_PATH = Path(__file__).resolve().parent / "price_cache.json"


def cache_key(crop: str, province: str) -> str:
    return f"{crop}|{province}"


def load_cache(path: str | Path | None = None) -> dict:
    p = Path(path or DEFAULT_CACHE_PATH)
    if not p.exists():
        return {}
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def save_cache(cache: dict, path: str | Path | None = None) -> None:
    p = Path(path or DEFAULT_CACHE_PATH)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2, ensure_ascii=False)


def rows_to_snapshots(crop: str, province: str, rows: list[dict]) -> list[PriceSnapshot]:
    return [
        PriceSnapshot(
            crop=crop,
            region=province,
            date=r["date"],
            price_idr_per_kg=r["price_idr_per_kg"],
        )
        for r in rows
    ]


def merge_rows(
    cache: dict, crop: str, province: str, rows: list[dict]
) -> dict:
    """Write-through merge: new rows win on date collisions, result stays
    date-sorted. Returns the mutated cache (also mutates in place)."""
    key = cache_key(crop, province)
    by_date = {r["date"]: r for r in cache.get(key, [])}
    for r in rows:
        by_date[r["date"]] = {"date": r["date"], "price_idr_per_kg": r["price_idr_per_kg"]}
    cache[key] = sorted(by_date.values(), key=lambda r: r["date"])
    return cache


def history_stats(prices: list[int]) -> dict | None:
    """Population mean/std of a price history + the ±2σ 'normal' band.
    Returns None if there aren't at least 2 points."""
    if len(prices) < 2:
        return None
    mu, sd = mean(prices), pstdev(prices)
    return {"mean": mu, "std": sd, "n": len(prices), "low": mu - 2 * sd, "high": mu + 2 * sd}


def override_price(
    conn: psycopg.Connection, crop: str, province: str, dt: str, price: int,
    cache_path: str | Path | None = None,
) -> dict | None:
    """Admin lever: set one day's price in BOTH the cache (what the engine
    reads) and the snapshot table. Returns the ±2σ stats of the PRIOR history
    (excluding this date) so the caller can judge 'beyond expectation'.

    Reversible: re-import the real CSVs (`rm price_cache.json && python -m
    scripts.import_bi_csv`) then reseed to wipe the override.
    """
    cache = load_cache(cache_path)
    key = cache_key(crop, province)
    stats = history_stats([r["price_idr_per_kg"] for r in cache.get(key, []) if r["date"] != dt])
    merge_rows(cache, crop, province, [{"date": dt, "price_idr_per_kg": price}])
    save_cache(cache, cache_path)
    conn.execute(
        "INSERT INTO price_snapshot (crop, region, date, price_idr_per_kg)"
        " VALUES (%s, %s, %s, %s)"
        " ON CONFLICT(crop, region, date) DO UPDATE SET"
        " price_idr_per_kg = excluded.price_idr_per_kg",
        (crop, province, dt, price),
    )
    conn.commit()
    return stats


def restore_real_prices(
    conn: psycopg.Connection, uploads_dir, cache_path: str | Path | None = None
) -> int:
    """Undo any /admin override: rebuild the cache from the real BI CSVs, then
    replace the whole price_snapshot table from it. Touches ONLY prices — the
    farmer/harvest_report/match_request demo data is left intact. Returns the
    number of snapshot rows written."""
    from scripts.import_bi_csv import import_dir  # lazy: avoids import cycle

    p = Path(cache_path or DEFAULT_CACHE_PATH)
    if p.exists():
        p.unlink()
    import_dir(uploads_dir, cache_path)
    cache = load_cache(cache_path)
    conn.execute("DELETE FROM price_snapshot")  # drop overrides; real rows re-added below
    return sync_snapshots_table(conn, cache)


def sync_snapshots_table(conn: psycopg.Connection, cache: dict) -> int:
    """Mirror the cache into the price_snapshot table (queryable form)."""
    params = []
    for key, rows in cache.items():
        crop, province = key.split("|", 1)
        params.extend(
            (crop, province, r["date"], r["price_idr_per_kg"]) for r in rows
        )
    # executemany pipelines the statements — one round-trip per batch instead
    # of per row, which matters against the remote Supabase pooler now that
    # the cache holds full imported price histories.
    conn.cursor().executemany(
        "INSERT INTO price_snapshot (crop, region, date, price_idr_per_kg)"
        " VALUES (%s, %s, %s, %s)"
        " ON CONFLICT(crop, region, date) DO UPDATE SET"
        " price_idr_per_kg = excluded.price_idr_per_kg",
        params,
    )
    conn.commit()
    return len(params)
