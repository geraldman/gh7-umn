"""Import scraped PIHPS (Bank Indonesia) CSVs into data/price_cache.json.

Input: folders of ``*_data.csv`` files with columns
``Date,Region,RegionLevel,Commodity,Price`` (the ``*_stats.csv`` files are
ignored). Only province-level rows (RegionLevel == 1) are imported — the
"Semua Provinsi" national aggregate (level 0) is skipped.

Keys are slugified to match the cache convention, e.g.
``Cabai Rawit Merah`` + ``Jawa Tengah`` -> ``cabai_rawit_merah|jawa_tengah``.

Usage (from the repo root):

    python -m scripts.import_bi_csv [uploads_dir]

Then reseed (``python run.py --seed``) to mirror the cache into the
price_snapshot table — seed merges on top of the cache, it no longer wipes it.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

from data import loader


def _slug(s: str) -> str:
    return s.strip().lower().replace(" ", "_")


def import_dir(uploads_dir: str | Path, cache_path: str | Path | None = None) -> dict:
    """Merge every *_data.csv under uploads_dir into the cache. Returns
    {cache_key: rows_imported}."""
    cache = loader.load_cache(cache_path)
    imported: dict[str, int] = {}

    for csv_path in sorted(Path(uploads_dir).rglob("*_data.csv")):
        rows_by_key: dict[tuple[str, str], list[dict]] = {}
        with open(csv_path, encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                if row["RegionLevel"].strip() != "1":
                    continue  # skip the "Semua Provinsi" national aggregate
                key = (_slug(row["Commodity"]), _slug(row["Region"]))
                rows_by_key.setdefault(key, []).append(
                    {"date": row["Date"], "price_idr_per_kg": int(float(row["Price"]))}
                )
        for (crop, province), rows in rows_by_key.items():
            loader.merge_rows(cache, crop, province, rows)
            imported[loader.cache_key(crop, province)] = (
                imported.get(loader.cache_key(crop, province), 0) + len(rows)
            )

    loader.save_cache(cache, cache_path)
    return imported


if __name__ == "__main__":
    uploads = sys.argv[1] if len(sys.argv) > 1 else "uploads"
    imported = import_dir(uploads)
    if not imported:
        sys.exit(f"No *_data.csv files found under {uploads!r}")
    print(f"Merged into {loader.DEFAULT_CACHE_PATH}:")
    for key, n in sorted(imported.items()):
        print(f"  {key:<40} {n} rows")
    print("\nNow run `python run.py --seed` to mirror into the price_snapshot table.")
