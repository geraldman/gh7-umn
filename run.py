"""Panen Pas — one-command launcher.

    python run.py             start the Telegram bot (DB initialized if missing)
    python run.py --seed      re-seed the 3 demo scenarios first, then start
    python run.py --check     pre-demo ritual: seed + verify + tests, no bot

Requires the bot token, either in a `.env` file at the repo root (copy
`.env.example`) or as an environment variable:

    $env:TELEGRAM_BOT_TOKEN = "123456:ABC-..."     (PowerShell)
"""
from __future__ import annotations

import argparse
import io
import os
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env", override=False)

# Windows console: print emoji/± without UnicodeEncodeError (Telegram is
# unaffected either way; this is only for local log output).
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


def do_seed() -> bool:
    from data import seed as seeder

    conn = seeder.seed()
    print("Seeded. Verifying scenarios:")
    ok = True
    for name, expected, result in seeder.verify(conn):
        got = result["recommendation"]
        ok &= got == expected
        print(f"  [{'OK' if got == expected else 'FAIL'}] {name:<10}"
              f" expected={expected:<4} got={got}")
    return ok


def main() -> int:
    parser = argparse.ArgumentParser(description="Panen Pas launcher")
    parser.add_argument("--seed", action="store_true",
                        help="re-seed the demo scenarios before starting the bot")
    parser.add_argument("--check", action="store_true",
                        help="pre-demo ritual: seed + verify + run tests, don't start the bot")
    args = parser.parse_args()

    if args.check:
        # Tests first (they wipe the LOCAL docker Postgres), then seed —
        # so the database referenced by DATABASE_URL ends up demo-ready.
        print("Running test suite...")
        tests = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-q"])
        ok = tests.returncode == 0
        print()
        ok &= do_seed()
        print("\nPRE-DEMO CHECK PASSED — ready to run the bot."
              if ok else "\nPRE-DEMO CHECK FAILED — fix before demoing.")
        return 0 if ok else 1

    if args.seed:
        if not do_seed():
            print("Seed verification failed — not starting the bot.")
            return 1
        print()

    if not (os.environ.get("TELEGRAM_BOT_TOKEN") or os.environ.get("BOT_TOKEN")):
        print("ERROR: no bot token found. Either copy .env.example to .env and\n"
              "fill in TELEGRAM_BOT_TOKEN, or set it in this terminal (PowerShell):\n"
              '  $env:TELEGRAM_BOT_TOKEN = "paste-token-here"\n'
              "then run this again.")
        return 1

    from core import db

    print(f"Database: {os.environ.get('DB_TARGET', 'local')} ({db.describe_dsn()})")
    conn = db.get_connection()
    db.init_db(conn)  # no-op if tables exist; does NOT wipe data
    conn.close()

    from bot.bot import main as run_bot

    run_bot()
    return 0


if __name__ == "__main__":
    sys.exit(main())
