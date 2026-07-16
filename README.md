# Panen Pas 🌶️🧅

A Telegram bot that tells smallholder farmers **when to sell** their chili/shallot
harvest — by combining local oversupply detection (how many neighbors harvest the
same week) with regional price trends (PIHPS data) — and connects "sell now"
farmers to an anchor buyer automatically.

See `docs/ARCHITECTURE.md` for the full design.

## Prerequisites

- Python 3.10+
- Docker Desktop — runs the local Postgres (the test suite always uses it,
  even when the bot itself points at Supabase)
- Dependencies:

  ```powershell
  pip install -r requirements.txt          # runtime (python-telegram-bot)
  pip install -r requirements-dev.txt      # + pytest (needed for run.py --check)
  ```

## 1. Get a bot token (once)

1. In Telegram, message **@BotFather** → `/newbot` → follow the prompts.
2. Copy the token (looks like `123456789:AAE...`).
3. Put it in a `.env` file at the repo root (gitignored — **never commit it**):

   ```powershell
   copy .env.example .env      # then edit .env and paste your token
   ```

   Alternatively, an environment variable works too and takes precedence
   over `.env`:

   ```powershell
   $env:TELEGRAM_BOT_TOKEN = "paste-your-token-here"     # PowerShell
   ```

> If a token ever ends up in a committed file or a chat log, revoke it:
> @BotFather → `/revoke` → pick the bot → use the new token.

## 2. Database

`DB_TARGET` in `.env` toggles where data lives — flip one word to switch:

- **`DB_TARGET=local`** (default) — the docker Postgres:

  ```powershell
  docker compose up -d db     # Postgres on localhost:5433, data persists
  ```

- **`DB_TARGET=supabase`** — the shared team DB. Fill `DATABASE_URL_SUPABASE`
  with the **Session Pooler** connection string from Dashboard → Connect
  (host like `aws-0-<region>.pooler.supabase.com`, port 5432). Don't use the
  "direct connection" string — it is IPv6-only and fails on most networks.

`run.py` prints which database it is using at startup — glance at that line
before demoing.

The test suite **always** runs against the local container (it wipes every
table, so it refuses to touch Supabase) — start it before `run.py --check`.

## 3. Run

Everything goes through one launcher at the repo root:

| Command | What it does |
|---|---|
| `python run.py` | Start the bot (initializes the DB if missing; never wipes data) |
| `python run.py --seed` | Re-seed the 3 demo scenarios + verify them, then start the bot |
| `python run.py --check` | Pre-demo ritual: seed → verify scenarios → run all tests. No bot. |

No server or hosting needed — the bot uses **long polling**, so your laptop *is*
the server. It works behind any Wi-Fi/NAT with no public IP.

**Or run everything in Docker** (same `.env`, nothing else to install):

```powershell
docker compose up -d bot                            # build + start (uses .env)
docker compose logs -f bot                          # watch it
docker compose run --rm bot python -m data.seed     # seed + verify scenarios
docker compose stop bot                             # stop it
```

⚠️ Only **one** process may poll the token — stop the docker bot before
running `python run.py` on the host (and vice versa).

## 4. Using the bot

Everyone starts with `/start` and picks a role:

- **👨‍🌾 Petani (farmer)** — answers four questions, all by tapping buttons or
  typing a number: crop → district → days to harvest → estimated kg → confirm.
  Gets a recommendation (🟢 jual / 🟡 jadwal biasa / 🔵 tunggu) with the price
  date and the reasoning. On "jual", the offer is pushed to the buyer.
- **🏪 Pembeli (anchor buyer)** — register *before* farmers report; receives a
  match card with **✅ Terima / ❌ Tolak** buttons for each "sell" offer. Either
  choice notifies the farmer.
- **📋 Koordinator** — `/status` lists every match and its state.

`/cancel` aborts a conversation at any point.

## 5. Demo-day script

```powershell
docker compose up -d db     # local Postgres (tests need it)
python run.py --check       # everything green? then:
python run.py --seed        # fresh scenarios + bot up
```

(Token and database come from `.env` — nothing to set in the terminal.
If demoing on Supabase: open the dashboard in the morning to un-pause the
project — the free tier sleeps after ~a week idle.)

The three seeded scenarios (dates are always relative to today — re-seeding
keeps them fresh):

| Report this as farmer | Expected result |
|---|---|
| Cabai Merah, **Garut**, 2 days | 🟢 **sell** + buyer match (4 seeded neighbors + falling price) |
| Bawang Merah, **Brebes**, 2 days | 🔵 **wait** (no neighbors, rising price) |
| Bawang Merah, **Cianjur**, 2 days | 🟡 **hold** (1 neighbor, flat price) |

Also rehearse the failure paths: type a random crop (`durian`) → the bot
re-prompts with buttons instead of crashing; have the buyer tap **Tolak** →
the farmer gets a graceful notification.

## 6. Price data modes

| Mode | Behavior |
|---|---|
| `PRICE_SOURCE=cache` (default) | Prices from `data/price_cache.json` — zero network, demo-safe |
| `PRICE_SOURCE=live` | Try PIHPS → Panel Harga → cache, in order, with timeouts |

The live sources are stubs until their endpoints are captured (see
`data/sources.py` TODOs) — with `live` set today, the chain simply falls
through to the cache.

## Troubleshooting

- **"no bot token found"** — make sure `.env` exists at the repo root (copy
  `.env.example`) and contains `TELEGRAM_BOT_TOKEN=...` with no quotes needed.
- **Bot doesn't reply** — only one process may poll a given token at a time;
  make sure a teammate isn't also running the bot with the same token.
- **"connection refused" / database errors** — local mode: start the DB with
  `docker compose up -d db` (and give it a few seconds on first boot).
  Supabase mode: check the project isn't paused and that `DATABASE_URL` is
  the Session Pooler string, not the direct one.
- **Emoji garbled in the terminal** — cosmetic only (Windows console encoding);
  Telegram messages are unaffected.
- **Scenarios give wrong results** — the seeds age relative to today; run
  `python run.py --seed` to refresh, and check `python run.py --check`.

## Project layout

```
run.py             ← the launcher (start here)
docker-compose.yml local Postgres (offline fallback + test database)
core/              rule engine, Postgres, orchestrator   (channel-agnostic)
data/              price sources, cache, demo seeds
bot/               Telegram adapter (conversation, formatting, roles)
tests/             49 tests — python -m pytest tests/ -q
docs/              ARCHITECTURE.md
```
