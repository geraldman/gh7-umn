# Bot adapter

See the **root `README.md`** for setup and run instructions — everything goes
through `python run.py` at the repo root.

This folder is the Telegram adapter layer (ARCHITECTURE.md §6): conversation
flow, Bahasa Indonesia formatting, and role handling. It is deliberately thin —
all business logic lives in `core/`, and the only write path into core data is
`core.api.process_harvest_report()`.

> Historical note: the original README here described an earlier design
> (in-memory match storage, `BUYER_CHAT_ID` env var, a mock rule engine).
> That design was replaced on 2026-07-16 when the bot was wired to the real
> engine and SQLite. Buyer registration now happens in-chat via /start.
