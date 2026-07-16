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


def sync_snapshots_table(conn: psycopg.Connection, cache: dict) -> int:
    """Mirror the cache into the price_snapshot table (queryable form)."""
    n = 0
    for key, rows in cache.items():
        crop, province = key.split("|", 1)
        for r in rows:
            conn.execute(
                "INSERT INTO price_snapshot (crop, region, date, price_idr_per_kg)"
                " VALUES (%s, %s, %s, %s)"
                " ON CONFLICT(crop, region, date) DO UPDATE SET"
                " price_idr_per_kg = excluded.price_idr_per_kg",
                (crop, province, r["date"], r["price_idr_per_kg"]),
            )
            n += 1
    conn.commit()
    return n
