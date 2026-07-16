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
