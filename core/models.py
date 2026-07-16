"""Canonical vocabulary and data shapes for Panen Pas.

This module is the single source of truth for valid crop/region keys
(ARCHITECTURE.md §2). The Telegram adapter imports these constants to build
its keyboards and normalization ladder; the orchestrator validates against
them. Nothing else defines vocabulary anywhere.
"""
from __future__ import annotations

from dataclasses import dataclass

# --- Canonical vocabulary ---------------------------------------------------

CROPS = {"cabai_merah", "bawang_merah"}

# Keys are the valid *district* (kecamatan/kabupaten) region codes farmers
# report from; values are the province whose PIHPS price series applies.
# Clustering runs on the district key; price lookup runs on the province.
# Adding a region = one row here + loading that province's price history.
REGION_TO_PROVINCE = {
    "garut": "jawa_barat",
    "cianjur": "jawa_barat",
    "brebes": "jawa_tengah",
}

# --- Data shapes (mirror the SQLite schema, ARCHITECTURE.md §3) --------------


@dataclass
class Farmer:
    id: int | None
    telegram_id: str | None
    name: str | None
    region: str  # district key


@dataclass
class HarvestReport:
    id: int | None
    farmer_id: int
    crop: str
    region: str  # district key
    harvest_date: str  # ISO date
    quantity_kg: float | None
    created_at: str | None = None


@dataclass
class PriceSnapshot:
    crop: str
    region: str  # province key (price data is province-level)
    date: str  # ISO date
    price_idr_per_kg: int


@dataclass
class MatchRequest:
    id: int | None
    harvest_report_id: int
    buyer_id: int = 1
    status: str = "pending"  # pending | confirmed | declined
    created_at: str | None = None
