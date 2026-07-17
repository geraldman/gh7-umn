"""The rule engine (ARCHITECTURE.md §4).

Two layers:
- decide()             — the rule table as a pure function. No DB, no I/O.
                         This is where the exhaustive unit tests live.
- get_recommendation() — gathers signals (cluster + trend) and calls decide().
                         Read-only: never writes anything, safe to call twice.

The single write path is core.api.process_harvest_report() — the bot calls
that, not these.
"""
from __future__ import annotations

from datetime import date, timedelta

import psycopg

from core import db
from core.clustering import count_cluster
from core.models import CROPS, REGION_TO_PROVINCE
from core.price_trend import get_trend

CROWDED_THRESHOLD = 3  # reports within ±2 days, INCLUDING the new one


def decide(
    trend: str,
    cluster_size: int,
    days_to_harvest: int,
    pct_change: float | None = None,
) -> dict:
    """The rule table. Returns {"recommendation": "sell"|"hold"|"wait", "reason": str}."""
    crowded = cluster_size >= CROWDED_THRESHOLD
    pct = f" ({pct_change:+.1f}%)" if pct_change is not None else ""

    if trend == "falling" and crowded:
        rec, reason = "sell", (
            f"Price falling{pct} and {cluster_size} farmers harvesting within "
            f"±2 days — sell now before the local oversupply makes it worse."
        )
    elif trend == "falling":
        rec, reason = "sell", f"Price falling{pct} — sell before it drops further."
    elif trend == "flat" and crowded:
        rec, reason = "sell", (
            f"{cluster_size} farmers harvesting within ±2 days will push the "
            f"local price down even though the market is flat — sell before the glut."
        )
    elif trend == "flat":
        rec, reason = "hold", (
            "No price pressure and no harvest cluster — sell on your normal schedule."
        )
    elif trend == "rising" and crowded:
        rec, reason = "hold", (
            f"Price rising{pct} but {cluster_size} nearby harvests are coming — "
            f"hold briefly, don't wait long."
        )
    else:  # rising, not crowded
        rec, reason = "wait", (
            f"Price rising{pct} and no local glut — waiting a few days should pay off."
        )

    # Override: the crop can't wait (ARCHITECTURE.md §4).
    if days_to_harvest <= 1:
        if rec == "wait":
            rec = "hold"
            reason += " Harvest is imminent, so don't delay past a day or two."
        elif rec == "hold" and trend == "falling":
            rec = "sell"
            reason += " Harvest is imminent and the price is falling — sell."

    return {"recommendation": rec, "reason": reason}


def get_recommendation(
    crop: str,
    region: str,
    days_to_harvest: int,
    *,
    conn: psycopg.Connection | None = None,
    chain=None,
    today: date | None = None,
) -> dict:
    """Read-only signal gathering + decide(). The contract function.

    Unknown keys never crash and never fabricate a trend: honest "hold".
    Extra keys beyond the contract ({recommendation, reason}) are additive:
    price_source, price_as_of, cluster_size, trend.
    """
    if crop not in CROPS:
        return {
            "recommendation": "hold",
            "reason": f"unknown crop '{crop}' — no price data available",
        }
    if region not in REGION_TO_PROVINCE:
        return {
            "recommendation": "hold",
            "reason": f"unknown region '{region}' — no data available",
        }

    from data import sources  # late import: keeps core importable without data pkg config

    conn = conn if conn is not None else db.get_connection()
    chain = chain if chain is not None else sources.build_default_chain()
    today = today or date.today()

    harvest_date = today + timedelta(days=days_to_harvest)
    cluster_size = count_cluster(conn, crop, region, harvest_date)

    province = REGION_TO_PROVINCE[region]
    prices, source_name = chain.fetch(crop, province)
    trend_info = get_trend(prices)

    result = decide(
        trend_info["trend"], cluster_size, days_to_harvest, trend_info["pct_change"]
    )
    result["trend"] = trend_info["trend"]
    result["cluster_size"] = cluster_size
    result["price_source"] = source_name
    result["price_as_of"] = trend_info["latest_date"]
    result["price_latest"] = trend_info.get("latest_price")
    result["pct_change"] = trend_info["pct_change"]
    return result
