"""Tests for count_cluster() — sliding ±2 day window, crop+district."""
from __future__ import annotations

from datetime import timedelta

from core.clustering import count_cluster
from tests.conftest import TODAY, insert_report

HD = TODAY + timedelta(days=2)  # the queried harvest date


def test_empty_region_counts_zero(conn):
    assert count_cluster(conn, "cabai_merah", "garut", HD) == 0


def test_same_day_reports_cluster(conn):
    insert_report(conn, 1, "cabai_merah", "garut", HD)
    insert_report(conn, 1, "cabai_merah", "garut", HD)
    assert count_cluster(conn, "cabai_merah", "garut", HD) == 2


def test_window_edges_inclusive(conn):
    insert_report(conn, 1, "cabai_merah", "garut", HD - timedelta(days=2))
    insert_report(conn, 1, "cabai_merah", "garut", HD + timedelta(days=2))
    assert count_cluster(conn, "cabai_merah", "garut", HD) == 2


def test_outside_window_excluded(conn):
    insert_report(conn, 1, "cabai_merah", "garut", HD - timedelta(days=3))
    insert_report(conn, 1, "cabai_merah", "garut", HD + timedelta(days=3))
    assert count_cluster(conn, "cabai_merah", "garut", HD) == 0


def test_different_crop_not_counted(conn):
    insert_report(conn, 1, "bawang_merah", "garut", HD)
    assert count_cluster(conn, "cabai_merah", "garut", HD) == 0


def test_different_district_not_counted(conn):
    insert_report(conn, 1, "cabai_merah", "cianjur", HD)
    assert count_cluster(conn, "cabai_merah", "garut", HD) == 0


def test_window_slides_per_report(conn):
    """Farmer A (day 2) and farmer B (day 6) are not in each other's cluster."""
    insert_report(conn, 1, "cabai_merah", "garut", TODAY + timedelta(days=2))
    insert_report(conn, 1, "cabai_merah", "garut", TODAY + timedelta(days=6))
    assert count_cluster(conn, "cabai_merah", "garut", TODAY + timedelta(days=2)) == 1
    assert count_cluster(conn, "cabai_merah", "garut", TODAY + timedelta(days=6)) == 1
    # ...but day 4 sees both edges
    assert count_cluster(conn, "cabai_merah", "garut", TODAY + timedelta(days=4)) == 2
