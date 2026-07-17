"""Bot configuration.

The token is read from the environment, which may be populated from a `.env`
file at the repo root (gitignored — see `.env.example`):

    TELEGRAM_BOT_TOKEN=123456:ABC-...

A real environment variable always wins over the `.env` file.
"""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# Repo-root .env; override=False means a real env var beats the file.
load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=False)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN") or os.environ.get("BOT_TOKEN")

# Who may use /admin. Match by numeric id (robust) OR by @username (handy).
# BOTH unset => /admin is disabled for everyone (fail-safe: never leave the
# price override open).
def _int_env(name: str) -> int:
    """Tolerant int env read: a non-numeric value (e.g. a username pasted into
    the wrong field) yields 0, not a crash at import time."""
    try:
        return int(os.environ.get(name) or 0)
    except ValueError:
        return 0


ADMIN_TELEGRAM_ID = _int_env("ADMIN_TELEGRAM_ID")
ADMIN_USERNAME = (os.environ.get("ADMIN_USERNAME") or "").lstrip("@").lower()
