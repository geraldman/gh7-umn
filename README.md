# Panen Pas 🌶️🧅

A Telegram bot that tells smallholder chili farmers (**Cabai Rawit Merah**) **when
to sell** their harvest. It combines two signals:

- **Local oversupply** — how many neighbouring farmers report harvesting the same
  crop in the same district within a ±2-day window.
- **Price trend** — whether the regional price is rising, flat, or falling.

A rule engine turns those into 🟢 *jual* (sell) / 🟡 *jadwal biasa* (hold) /
🔵 *tunggu* (wait). When the answer is **sell**, the bot pushes an offer to a
registered anchor buyer, who accepts or declines — and the farmer is notified
either way.

See `docs/ARCHITECTURE.md` for the full design.

---

## Setup

### Prerequisites

- **Python 3.10+** (developed on 3.14)
- **Docker Desktop** — runs Postgres. Required for the local database and for the
  test suite even when the bot itself points at Supabase.

### 1. Install dependencies

```powershell
pip install -r requirements.txt          # runtime: python-telegram-bot, psycopg, dotenv
pip install -r requirements-dev.txt      # + pytest (only needed for run.py --check)
```

*(Skip this entirely if you only ever run via Docker — the image installs its own.)*

### 2. Create your `.env`

All configuration — the bot token and the database — lives in one gitignored
`.env` file at the repo root. Copy the template:

```powershell
copy .env.example .env
```

Then edit `.env`:

```ini
TELEGRAM_BOT_TOKEN=123456789:AAE...        # from @BotFather (see below)

DB_TARGET=local                            # "local" or "supabase" — the toggle
DATABASE_URL_LOCAL=postgresql://postgres:postgres@localhost:5433/panen
DATABASE_URL_SUPABASE=                     # paste Session Pooler string here
```

> ⚠️ **No inline comments in `.env`** (`KEY=value # note`). Docker reads the file
> literally, so the `# note` becomes part of the value and breaks it. Keep each
> line as `KEY=value` only.

**Get a bot token** (once): message **@BotFather** → `/newbot` → follow the
prompts → copy the token into `TELEGRAM_BOT_TOKEN`. If a token ever leaks (into a
commit, a log, a screenshot), revoke it: @BotFather → `/mybots` → pick the bot →
**API Token → Revoke**.

### 3. Choose a database

`DB_TARGET` flips between two databases — change one word, no code edits:

| `DB_TARGET` | Where data lives | Setup |
|---|---|---|
| `local` (default) | Docker Postgres on `localhost:5433`, data persists in a volume | `docker compose up -d db` |
| `supabase` | The shared team database | Fill `DATABASE_URL_SUPABASE` (see below) |

**Supabase string:** Dashboard → **Connect** → **Session Pooler** (host like
`aws-0-<region>.pooler.supabase.com`, port **5432**). Do **not** use the "Direct
connection" string — it is IPv6-only and fails on most Wi-Fi/campus networks.

Both `run.py` and the Docker bot print which database they are using at
startup — glance at that line before demoing.

---

## Running

### Option A — on your machine

```powershell
docker compose up -d db     # if DB_TARGET=local (tests need this either way)
python run.py               # start the bot
```

| Command | What it does |
|---|---|
| `python run.py` | Start the bot (creates tables if missing; never wipes data) |
| `python run.py --seed` | Re-seed the 3 demo scenarios + verify them, then start |
| `python run.py --check` | Pre-demo ritual: run all tests → seed → verify. No bot. |

The bot uses **long polling**, so your laptop *is* the server — no hosting, no
public IP, works behind any NAT.

### Option B — fully in Docker

Same `.env`, nothing else to install:

```powershell
docker compose up -d bot                            # build + start
docker compose logs -f bot                          # watch it
docker compose run --rm bot python -m data.seed     # seed + verify scenarios
docker compose stop bot                             # stop it
```

After editing `.env`, recreate the container so it picks up the changes:

```powershell
docker compose up -d --force-recreate bot
```

> ⚠️ **One poller per token.** Telegram allows only one process to long-poll a
> given token at a time. Don't run the Docker bot and `python run.py` at once —
> stop one before starting the other.

---

## Using the bot

Everyone sends `/start` and picks a role (inline buttons):

- **👨‍🌾 Petani (farmer)** — answers: crop → district → days to harvest →
  estimated kg → phone number → confirm. Crop, district, and the confirmation are
  tap-a-button; days, kg, and phone are typed. Typing also works as a fallback
  everywhere. Returns a recommendation (real price + reasoning); on **sell**, the
  offer is pushed to the buyer. Re-reporting the same harvest the same day asks
  whether to **add** or **replace** the quantity.
- **🏪 Pembeli (anchor buyer)** — picks an operating region at sign-up, then lands
  straight in the harvest browser. Gets a match card with **✅ Terima / ❌ Tolak**
  for each sell offer (either choice notifies the farmer), and can use **/panen**
  to browse harvests per district and place a bulk buy — the system fills the
  order across farmers (earliest-harvest first) and notifies each seller.
- **📋 Koordinator** — `/status` lists every match and its state.

`/help` shows all commands; `/cancel` aborts a conversation at any point.

---

## Demo-day script

```powershell
docker compose up -d db     # local Postgres (tests need it)
python run.py --check       # all green? then:
python run.py --seed        # fresh scenarios + bot up
```

The two seeded scenarios (dates are relative to today — re-seeding keeps them
fresh; prices are **real Bank Indonesia data**, currently flat, so the sell
signal comes from the local harvest cluster):

| Report this as farmer | Expected result |
|---|---|
| Cabai Rawit Merah, **Garut**, 2 days | 🟢 **sell** + buyer match (4 seeded neighbours harvesting together — a local glut even though the market is flat) |
| Cabai Rawit Merah, **Cianjur**, 2 days | 🟡 **hold** (no cluster, flat price) |

The third case — 🔵 **wait** (rising price, no glut) — can't be seeded from real
data (no series is rising this week), so it's covered by the unit tests instead.

Also rehearse the failure paths: type a nonsense crop (`durian`) → the bot
re-prompts with buttons instead of crashing; have the buyer tap **Tolak** → the
farmer gets a graceful notification.

> Note: a farmer re-reporting the same crop+district within ±2 days **updates**
> the first report and won't create a second buyer match (the double-sell guard).
> To re-run a scenario cleanly, re-seed: `docker compose run --rm bot python -m data.seed`.

If demoing on **Supabase**, open the dashboard the morning of — the free tier
pauses a project after ~a week idle, and a paused DB on stage is a demo killer.

---

## Price data

The engine reads price history through a **swappable source chain** in
`data/sources.py` (`PRICE_SOURCE=cache` by default → `data/price_cache.json`,
zero network, demo-safe).

Two Indonesian government sources were investigated for live data — **both are
behind anti-bot protection** and can't be scraped with a plain HTTP client:

| Source | Access | Price level |
|---|---|---|
| **Panel Harga** (Badan Pangan) | `x-api-key` → 401 (runtime-signed / reCAPTCHA-bound) | **producer / petani** ✅ |
| **PIHPS** (Bank Indonesia) | data endpoints 302 → error page (WAF) | consumer / retail |

**Recommended path for real data:** capture it once from a real browser
(DevTools → Network → right-click the data request → **Copy as cURL**), which
carries the session/signed headers, then convert the JSON into
`data/price_cache.json`. Panel Harga is the better target — producer-level prices
are the correct signal for a farmer's sell decision. This keeps the demo off the
live network entirely.

---

## Troubleshooting

- **"no bot token found"** — `.env` must exist at the repo root and contain
  `TELEGRAM_BOT_TOKEN=...` (no quotes needed).
- **Bot doesn't reply** — only one process may poll a token at a time; make sure
  a teammate (or a leftover Docker container) isn't polling the same token. Also
  confirm you're messaging the *right* bot — the token decides which one.
- **Database / "connection refused"** — local: `docker compose up -d db` and give
  it a few seconds on first boot. Supabase: check the project isn't paused and
  that you used the **Session Pooler** string, not the direct one.
- **Docker bot ignores an `.env` change** — recreate it:
  `docker compose up -d --force-recreate bot`.
- **`DB_TARGET must be 'local' or 'supabase'`** — you have an inline `# comment`
  on that line in `.env`; remove it.
- **Emoji garbled in the terminal** — cosmetic Windows-console encoding only;
  Telegram messages are unaffected.
- **Scenarios give wrong results** — seeds age relative to today; re-run
  `python run.py --seed`.

---

## Project layout

```
run.py             ← the launcher (start here)
Dockerfile         bot image (python:3.13-slim)
docker-compose.yml Postgres (db) + bot services
.env               your token + database config (gitignored)
core/              rule engine, Postgres, orchestrator   (channel-agnostic)
data/              price sources, cache, demo seeds
bot/               Telegram adapter (conversation, formatting, roles)
tests/             54 tests — python -m pytest tests/ -q
docs/              ARCHITECTURE.md
```
