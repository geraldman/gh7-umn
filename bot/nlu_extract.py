"""Free-text normalization — tier 2 of the input ladder (ARCHITECTURE.md §2).

Tier 1 is buttons (preferred, input already canonical); this alias map is the
typed-input backup. Tier 3 (LLM parse, LLM_PARSE=on) is not implemented yet;
tier 4 (re-prompt with buttons) lives in the conversation handlers.

NOTE: never put secrets (bot tokens etc.) in this or any tracked file — use
the TELEGRAM_BOT_TOKEN environment variable (see bot/config.py).
"""
from __future__ import annotations

from core.models import CROPS, REGION_TO_PROVINCE

CROP_ALIASES = {
    "cabai": "cabai_merah",
    "cabe": "cabai_merah",
    "cabai merah": "cabai_merah",
    "cabe merah": "cabai_merah",
    "lombok": "cabai_merah",
    "chili": "cabai_merah",
    "bawang": "bawang_merah",
    "bawang merah": "bawang_merah",
    "brambang": "bawang_merah",
    "shallot": "bawang_merah",
}


def normalize_crop(text: str) -> str | None:
    key = text.strip().lower().replace("_", " ")
    canonical = key.replace(" ", "_")
    if canonical in CROPS:
        return canonical
    return CROP_ALIASES.get(key)


def normalize_region(text: str) -> str | None:
    key = text.strip().lower().replace(" ", "_")
    return key if key in REGION_TO_PROVINCE else None
