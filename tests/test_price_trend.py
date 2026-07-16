"""Tests for get_trend() — data-anchored windows (ARCHITECTURE.md §4)."""
from __future__ import annotations

from datetime import date, timedelta

from core.price_trend import get_trend
from tests.conftest import FALLING, FLAT, RISING, TODAY, make_series


def test_falling_series():
    t = get_trend(make_series(FALLING))
    assert t["trend"] == "falling"
    assert t["pct_change"] < -5


def test_rising_series():
    t = get_trend(make_series(RISING))
    assert t["trend"] == "rising"
    assert t["pct_change"] > 5


def test_flat_series():
    t = get_trend(make_series(FLAT))
    assert t["trend"] == "flat"


def test_boundary_exactly_plus_5_is_flat():
    # prev 4 days at 40000, recent 3 at 42000 → exactly +5.0% → flat (strict >)
    t = get_trend(make_series([40000] * 4 + [42000] * 3))
    assert t["pct_change"] == 5.0
    assert t["trend"] == "flat"


def test_boundary_exactly_minus_5_is_flat():
    t = get_trend(make_series([40000] * 4 + [38000] * 3))
    assert t["pct_change"] == -5.0
    assert t["trend"] == "flat"


def test_empty_series_is_flat_with_note():
    t = get_trend([])
    assert t["trend"] == "flat"
    assert t["pct_change"] is None
    assert t["latest_date"] is None
    assert "insufficient" in t["note"]


def test_four_data_days_is_insufficient():
    t = get_trend(make_series([40000, 41000, 42000, 43000]))
    assert t["trend"] == "flat"
    assert "insufficient" in t["note"]


def test_five_data_days_is_enough():
    # 2 prev days @40000, 3 recent @45000 → +12.5% rising
    t = get_trend(make_series([40000, 40000, 45000, 45000, 45000]))
    assert t["trend"] == "rising"


def test_gaps_count_data_days_not_calendar_days():
    # 7 data points spread over 14 calendar days (every other day)
    prices = FALLING
    start = TODAY - timedelta(days=14)
    series = make_series([prices[0]])  # placeholder to reuse shape
    series = [
        type(series[0])(
            "cabai_merah",
            "jawa_barat",
            (start + timedelta(days=i * 2)).isoformat(),
            p,
        )
        for i, p in enumerate(prices)
    ]
    t = get_trend(series)
    assert t["trend"] == "falling"


def test_stale_series_still_computes_and_reports_its_date():
    old_end = TODAY - timedelta(days=10)
    t = get_trend(make_series(FALLING, end=old_end))
    assert t["trend"] == "falling"
    assert t["latest_date"] == old_end.isoformat()  # honesty: "harga per <date>"


def test_duplicate_dates_are_averaged_not_double_counted():
    series = make_series(FALLING) + make_series(FALLING)  # every date twice
    t = get_trend(series)
    assert t["trend"] == "falling"
