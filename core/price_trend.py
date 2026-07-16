"""Price trend: rising / flat / falling from a price series (ARCHITECTURE.md §4).

Windows are anchored to the LATEST DATE IN THE DATA, never date.today(), so a
stale cache still computes honestly. Windows count *data days*, not calendar
days — market-holiday gaps don't break the math.
"""
from __future__ import annotations

from statistics import mean

from core.models import PriceSnapshot

RISING_PCT = 5.0
FALLING_PCT = -5.0
MIN_DATA_DAYS = 5
RECENT_WINDOW = 3  # last N data days
PREV_WINDOW = 4  # the up-to-N data days before that


def get_trend(prices: list[PriceSnapshot]) -> dict:
    """Returns {"trend": "rising"|"flat"|"falling",
                "pct_change": float | None,
                "latest_date": str | None,
                "note": str | None}.

    latest_date is exposed so the bot can honestly display "harga per <tanggal>".
    Fewer than MIN_DATA_DAYS distinct days -> "flat" with an honest note (the
    source chain normally guarantees ≥5 days; this is the terminal-cache /
    unknown-key escape hatch).
    """
    by_date: dict[str, list[int]] = {}
    for p in prices:
        by_date.setdefault(p.date, []).append(p.price_idr_per_kg)
    days = sorted(by_date)

    if len(days) < MIN_DATA_DAYS:
        return {
            "trend": "flat",
            "pct_change": None,
            "latest_date": days[-1] if days else None,
            "note": "insufficient price data — defaulting to flat",
        }

    daily = [mean(by_date[d]) for d in days]
    recent = daily[-RECENT_WINDOW:]
    prev = daily[-(RECENT_WINDOW + PREV_WINDOW):-RECENT_WINDOW]
    pct = (mean(recent) - mean(prev)) / mean(prev) * 100

    if pct > RISING_PCT:
        trend = "rising"
    elif pct < FALLING_PCT:
        trend = "falling"
    else:
        trend = "flat"
    return {
        "trend": trend,
        "pct_change": round(pct, 1),
        "latest_date": days[-1],
        "note": None,
    }
