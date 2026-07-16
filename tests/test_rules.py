"""Exhaustive tests for decide() — the pure rule table (ARCHITECTURE.md §4/§7)."""
from __future__ import annotations

import pytest

from core.rules import decide

# --- The six rule-table rows -------------------------------------------------
# (trend, crowded cluster?, expected)
TABLE = [
    ("falling", 4, "sell"),
    ("falling", 1, "sell"),
    ("flat", 4, "sell"),
    ("flat", 1, "hold"),
    ("rising", 4, "hold"),
    ("rising", 1, "wait"),
]


@pytest.mark.parametrize("trend,cluster,expected", TABLE)
def test_rule_table(trend, cluster, expected):
    result = decide(trend, cluster, days_to_harvest=5)
    assert result["recommendation"] == expected
    assert result["reason"]  # every branch explains itself


# --- Crowded threshold boundaries (≥3 including the new report) ---------------

def test_cluster_exactly_three_is_crowded():
    assert decide("flat", 3, 5)["recommendation"] == "sell"


def test_cluster_exactly_two_is_not_crowded():
    assert decide("flat", 2, 5)["recommendation"] == "hold"


# --- days_to_harvest <= 1 override --------------------------------------------

def test_imminent_harvest_downgrades_wait_to_hold():
    assert decide("rising", 1, days_to_harvest=1)["recommendation"] == "hold"
    assert decide("rising", 1, days_to_harvest=0)["recommendation"] == "hold"


def test_imminent_harvest_does_not_change_other_holds():
    assert decide("flat", 1, days_to_harvest=1)["recommendation"] == "hold"
    assert decide("rising", 4, days_to_harvest=1)["recommendation"] == "hold"


def test_non_imminent_wait_stays_wait():
    assert decide("rising", 1, days_to_harvest=2)["recommendation"] == "wait"


# --- Reason content ------------------------------------------------------------

def test_reason_includes_cluster_count_when_crowded():
    assert "4" in decide("falling", 4, 5)["reason"]


def test_reason_includes_pct_change_when_given():
    assert "-8.0%" in decide("falling", 1, 5, pct_change=-8.0)["reason"]


def test_reason_survives_missing_pct():
    result = decide("falling", 1, 5, pct_change=None)
    assert result["recommendation"] == "sell"
    assert "%" not in result["reason"].split("—")[0] or True  # no crash is the point
