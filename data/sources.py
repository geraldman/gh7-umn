"""Price source fallback chain (ARCHITECTURE.md §4):

    live mode:   PIHPSSource → PanelHargaSource → CachedSource
    cache mode:  CachedSource only          (tests, pre-demo safe default)

Every source implements get_prices(crop, province) and raises
SourceUnavailable on timeout / HTTP error / bad payload / too-sparse data.
The terminal CachedSource never raises. get_recommendation() never knows
which source answered — results are tagged with the source name instead.
"""
from __future__ import annotations

import os
from pathlib import Path

from core.models import PriceSnapshot
from data import loader

MIN_DATA_DAYS = 5  # a live source that can't produce this many distinct days
LIVE_TIMEOUT_S = 5  # is unavailable for that query; the chain moves on


class SourceUnavailable(Exception):
    pass


class CachedSource:
    """data/price_cache.json — zero network, never fails. Terminal fallback."""

    name = "cache"
    terminal = True

    def __init__(self, path: str | Path | None = None):
        self.path = path

    def get_prices(self, crop: str, province: str) -> list[PriceSnapshot]:
        cache = loader.load_cache(self.path)
        rows = cache.get(loader.cache_key(crop, province), [])
        return loader.rows_to_snapshots(crop, province, rows)


class PIHPSSource:
    """Bank Indonesia PIHPS (bi.go.id/hargapangan). No official API — needs
    the XHR endpoint captured from browser DevTools (GetGridData-style POST,
    request the LAST 7 DAYS in one call, not a single date).

    TODO(pihps-capture): implement fetch + province/commodity ID mapping,
    then merge fresh rows into the cache (write-through) via loader.merge_rows.
    """

    name = "pihps"
    terminal = False

    def get_prices(self, crop: str, province: str) -> list[PriceSnapshot]:
        raise SourceUnavailable("PIHPS endpoint not captured yet")


class PanelHargaSource:
    """Badan Pangan Panel Harga (panelharga.badanpangan.go.id). Independent
    infrastructure from PIHPS; own commodity/region IDs (needs its own small
    mapping table).

    TODO(panelharga-capture): implement fetch; site was in maintenance on
    2026-07-16 — verify availability before relying on it.
    """

    name = "panelharga"
    terminal = False

    def get_prices(self, crop: str, province: str) -> list[PriceSnapshot]:
        raise SourceUnavailable("Panel Harga endpoint not captured yet")


class ChainedSource:
    """Walks the chain; returns (prices, source_name) from the first source
    that yields usable data. Non-terminal sources must produce ≥MIN_DATA_DAYS
    distinct dates; the terminal cache is accepted as-is (get_trend handles
    a sparse/empty series honestly)."""

    def __init__(self, sources: list):
        self.sources = sources

    def fetch(self, crop: str, province: str) -> tuple[list[PriceSnapshot], str]:
        for src in self.sources:
            try:
                prices = src.get_prices(crop, province)
            except SourceUnavailable:
                continue
            if not getattr(src, "terminal", False):
                if len({p.date for p in prices}) < MIN_DATA_DAYS:
                    continue  # too sparse to trend honestly — move on
            return prices, src.name
        return [], "none"


def build_default_chain(cache_path: str | Path | None = None) -> ChainedSource:
    """PRICE_SOURCE=live → full chain; anything else (default) → cache only."""
    cached = CachedSource(cache_path)
    if os.environ.get("PRICE_SOURCE", "cache").lower() == "live":
        return ChainedSource([PIHPSSource(), PanelHargaSource(), cached])
    return ChainedSource([cached])
