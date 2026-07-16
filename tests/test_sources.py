"""Tests for the price source fallback chain and cache loader."""
from __future__ import annotations

from core.models import PriceSnapshot
from data import loader
from data.sources import (
    CachedSource,
    ChainedSource,
    PanelHargaSource,
    PIHPSSource,
    SourceUnavailable,
)
from tests.conftest import FALLING, TODAY, make_series


class SparseLiveSource:
    name = "sparse"
    terminal = False

    def get_prices(self, crop, province):
        return make_series([40000, 41000])  # only 2 data days


class GoodLiveSource:
    name = "good"
    terminal = False

    def get_prices(self, crop, province):
        return make_series(FALLING)


def test_live_stubs_raise_unavailable():
    for src in (PIHPSSource(), PanelHargaSource()):
        try:
            src.get_prices("cabai_merah", "jawa_barat")
            assert False, "should have raised"
        except SourceUnavailable:
            pass


def test_chain_falls_through_stubs_to_cache(tmp_path):
    cache_path = tmp_path / "cache.json"
    cache: dict = {}
    rows = [{"date": p.date, "price_idr_per_kg": p.price_idr_per_kg}
            for p in make_series(FALLING)]
    loader.merge_rows(cache, "cabai_merah", "jawa_barat", rows)
    loader.save_cache(cache, cache_path)

    chain = ChainedSource([PIHPSSource(), PanelHargaSource(), CachedSource(cache_path)])
    prices, name = chain.fetch("cabai_merah", "jawa_barat")
    assert name == "cache"
    assert len(prices) == 7


def test_chain_skips_too_sparse_live_source(tmp_path):
    cache_path = tmp_path / "cache.json"
    loader.save_cache({}, cache_path)
    chain = ChainedSource([SparseLiveSource(), CachedSource(cache_path)])
    prices, name = chain.fetch("cabai_merah", "jawa_barat")
    assert name == "cache"  # sparse source rejected by the ≥5-day rule


def test_chain_prefers_healthy_live_source(tmp_path):
    chain = ChainedSource([GoodLiveSource(), CachedSource(tmp_path / "c.json")])
    prices, name = chain.fetch("cabai_merah", "jawa_barat")
    assert name == "good"
    assert len(prices) == 7


def test_cache_terminal_returns_empty_for_unknown_key(tmp_path):
    cache_path = tmp_path / "cache.json"
    loader.save_cache({}, cache_path)
    chain = ChainedSource([CachedSource(cache_path)])
    prices, name = chain.fetch("cabai_merah", "jawa_barat")
    assert prices == [] and name == "cache"  # get_trend handles [] honestly


def test_merge_rows_new_dates_win_and_stay_sorted():
    cache: dict = {}
    loader.merge_rows(cache, "c", "p", [
        {"date": "2026-07-02", "price_idr_per_kg": 100},
        {"date": "2026-07-01", "price_idr_per_kg": 200},
    ])
    loader.merge_rows(cache, "c", "p", [
        {"date": "2026-07-02", "price_idr_per_kg": 999},  # collision: new wins
    ])
    rows = cache["c|p"]
    assert [r["date"] for r in rows] == ["2026-07-01", "2026-07-02"]
    assert rows[1]["price_idr_per_kg"] == 999
