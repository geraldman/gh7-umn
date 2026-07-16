"""The seeder must produce the three expected demo outcomes — self-verifying."""
from __future__ import annotations

from data import seed
from tests.conftest import TODAY


def test_seed_scenarios_produce_expected_recommendations(tmp_path):
    db_path = tmp_path / "panen.db"
    cache_path = tmp_path / "price_cache.json"
    conn = seed.seed(db_path, cache_path, today=TODAY)
    for name, expected, result in seed.verify(conn, cache_path, today=TODAY):
        assert result["recommendation"] == expected, (
            f"{name}: expected {expected}, got {result['recommendation']}"
            f" ({result['reason']})"
        )


def test_seed_is_idempotent(tmp_path):
    db_path = tmp_path / "panen.db"
    cache_path = tmp_path / "price_cache.json"
    seed.seed(db_path, cache_path, today=TODAY)
    conn = seed.seed(db_path, cache_path, today=TODAY)  # run twice
    n_reports = conn.execute("SELECT COUNT(*) FROM harvest_report").fetchone()[0]
    n_farmers = conn.execute("SELECT COUNT(*) FROM farmer").fetchone()[0]
    assert n_reports == 5
    assert n_farmers == 6
