# Panen Pas 🌶️🧅

A Telegram bot that tells smallholder farmers **when to sell** their chili/shallot
harvest — by combining local oversupply detection (how many neighbors harvest the
same week) with regional price trends (PIHPS data) — and connects "sell now"
farmers to an anchor buyer automatically.

See `docs/ARCHITECTURE.md` for the full design.

## Prerequisites

- Python 3.10+
- Dependencies:

  ```powershell
  pip install -r requirements.txt          # pytest (core engine)
  pip install -r bot/requirements.txt      # python-telegram-bot
  ```

## 1. Get a bot token (once)

1. In Telegram, message **@BotFather** → `/newbot` → follow the prompts.
2. Copy the token (looks like `123456789:AAE...`).
3. Set it as an environment variable — **never paste it into a file in this repo**:

   ```powershell
   $env:TELEGRAM_BOT_TOKEN = "paste-your-token-here"     # PowerShell
   ```

   ```bash
   export TELEGRAM_BOT_TOKEN="paste-your-token-here"     # bash
   ```

> If a token ever ends up in a committed file or a chat log, revoke it:
> @BotFather → `/revoke` → pick the bot → use the new token.

## 2. Run

Everything goes through one launcher at the repo root:

| Command | What it does |
|---|---|
| `python run.py` | Start the bot (initializes the DB if missing; never wipes data) |
| `python run.py --seed` | Re-seed the 3 demo scenarios + verify them, then start the bot |
| `python run.py --check` | Pre-demo ritual: seed → verify scenarios → run all tests. No bot. |

No server or hosting needed — the bot uses **long polling**, so your laptop *is*
the server. It works behind any Wi-Fi/NAT with no public IP.

## 3. Using the bot

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

## 4. Demo-day script

```powershell
$env:TELEGRAM_BOT_TOKEN = "your-token"
python run.py --check       # everything green? then:
python run.py --seed        # fresh scenarios + bot up
```

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

## 5. Price data modes

| Mode | Behavior |
|---|---|
| `PRICE_SOURCE=cache` (default) | Prices from `data/price_cache.json` — zero network, demo-safe |
| `PRICE_SOURCE=live` | Try PIHPS → Panel Harga → cache, in order, with timeouts |

The live sources are stubs until their endpoints are captured (see
`data/sources.py` TODOs) — with `live` set today, the chain simply falls
through to the cache.

## Troubleshooting

- **"no bot token found"** — set `TELEGRAM_BOT_TOKEN` in the *same* terminal
  session you run `run.py` from (env vars don't persist across new windows).
- **Bot doesn't reply** — only one process may poll a given token at a time;
  make sure a teammate isn't also running the bot with the same token.
- **Emoji garbled in the terminal** — cosmetic only (Windows console encoding);
  Telegram messages are unaffected.
- **Scenarios give wrong results** — the seeds age relative to today; run
  `python run.py --seed` to refresh, and check `python run.py --check`.

## Project layout

```
run.py        ← the launcher (start here)
core/         rule engine, SQLite, orchestrator      (channel-agnostic)
data/         price sources, cache, demo seeds
bot/          Telegram adapter (conversation, formatting, roles)
tests/        49 tests — python -m pytest tests/ -q
docs/         ARCHITECTURE.md
```
