"""Bot configuration. The token comes from the environment ONLY — never from
a tracked file.

    $env:TELEGRAM_BOT_TOKEN = "123456:ABC-..."   (PowerShell)
"""
from __future__ import annotations

import os

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN") or os.environ.get("BOT_TOKEN")
