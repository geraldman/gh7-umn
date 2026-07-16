from __future__ import annotations

from datetime import date, timedelta

import pytest

from core import db
from core.models import PriceSnapshot

TODAY = date(2026, 7, 16)  # frozen — tests never depend on the wall clock


@pytest.fixture
def conn():
    c = db.get_connection(":memory:")
    db.init_db(c)
    for i in range(1, 6):  # farmers 1–5; tests use 1 as the caller, 2+ as neighbors
        c.execute(
            "INSERT INTO farmer (telegram_id, name, region) VALUES (?, ?, 'garut')",
            (f"tg-{i}", f"Test {i}"),
        )
    c.commit()
    yield c
    c.close()


class FakeChain:
    """Stands in for data.sources.ChainedSource in tests."""

    def __init__(self, prices: list[PriceSnapshot], name: str = "fake"):
        self.prices = prices
        self.name = name

    def fetch(self, crop, province):
        return self.prices, self.name


def make_series(
    prices: list[int],
    crop: str = "cabai_merah",
    province: str = "jawa_barat",
    end: date = TODAY - timedelta(days=1),
) -> list[PriceSnapshot]:
    """One PriceSnapshot per day, ending at `end`."""
    start = end - timedelta(days=len(prices) - 1)
    return [
        PriceSnapshot(crop, province, (start + timedelta(days=i)).isoformat(), p)
        for i, p in enumerate(prices)
    ]


FALLING = [50000, 49000, 48000, 47000, 44000, 43000, 42000]
RISING = [42000, 43000, 44000, 47000, 48000, 49000, 50000]
FLAT = [45000, 45200, 44800, 45000, 45100, 44900, 45000]


def insert_report(conn, farmer_id, crop, region, harvest_date: date, qty=100):
    conn.execute(
        "INSERT INTO harvest_report (farmer_id, crop, region, harvest_date,"
        " quantity_kg) VALUES (?, ?, ?, ?, ?)",
        (farmer_id, crop, region, harvest_date.isoformat(), qty),
    )
    conn.commit()
