# Panen Pas — Architecture

Panen Pas helps smallholder farmers (chili/shallot) decide **when to sell** by combining two signals:

1. **Supply clustering** — how many nearby farmers are harvesting the same crop at the same time (oversupply risk).
2. **Price trend** — whether the regional market price (PIHPS data) is rising, flat, or falling.

The output is a plain recommendation (`sell` / `hold` / `wait`) delivered through a Telegram bot, plus an automatic buyer-match request when the answer is "sell."

---

## 1. High-level structure

```
gh7-umn/
├── core/                    # Developer A — pure logic, no I/O framework deps
│   ├── models.py            # dataclasses: Farmer, HarvestReport, PriceSnapshot, MatchRequest
│   ├── db.py                # SQLite connection + schema init + CRUD helpers
│   ├── clustering.py        # cluster-detection (crop+region, ±2 day window)
│   ├── price_trend.py       # rising/flat/falling from cached price data
│   ├── rules.py             # decide() + get_recommendation() — the rule engine
│   ├── matching.py          # MatchRequest creation on "sell"
│   └── api.py               # process_harvest_report() — the orchestrator B calls
├── data/                    # Developer A — data assets
│   ├── price_cache.json     # cached PIHPS price history per crop+region
│   ├── sources.py           # PriceSource chain: PIHPS → Panel Harga → cache
│   ├── loader.py            # PIHPS export/scrape → price_cache.json
│   └── seed.py              # seeds the 3 demo scenarios into SQLite
├── adapters/
│   └── telegram/            # Developer B — everything bot-facing
│       ├── bot.py           # entry point, long polling
│       ├── farmer_flow.py   # conversation: crop → days-to-harvest → confirm
│       ├── buyer_flow.py    # anchor buyer confirms/declines pending matches
│       ├── formatting.py    # {recommendation, reason} → Bahasa Indonesia message
│       └── status.py        # /status coordinator command
├── tests/
│   └── test_rules.py        # unit tests against the seeded scenarios
├── panen.db                 # SQLite database (gitignored)
└── ARCHITECTURE.md
```

**Ownership boundary:** Developer A owns `/core`, `/data`, `/tests`. Developer B owns `/adapters/telegram`. The only surface they share is the merge contract below. Neither side imports across the boundary except Developer B calling `core.rules.get_recommendation()`.

---

## 2. The merge contract

Agreed before any code is written. Both sides build against this with mocks until merge.

### Entry point (what Developer B calls)

```python
def process_harvest_report(farmer_id: int, crop: str, region: str,
                           days_to_harvest: int, quantity_kg: float) -> dict:
    """Inserts the HarvestReport, runs the rules, creates a MatchRequest on "sell".
    Returns {"recommendation": "sell" | "hold" | "wait", "reason": str}"""
```

This is the **single write path** — the bot never inserts core rows itself. B's mock
must match this signature from day one; the swap at merge is still one line.

Internally it layers onto two read-only functions (both Developer A's):

```python
# core/rules.py
def decide(trend: str, cluster_size: int, days_to_harvest: int) -> dict:
    """Pure rule table — no DB, no I/O. Where the unit tests live."""

def get_recommendation(crop: str, region: str, days_to_harvest: int) -> dict:
    """Gathers signals (trend + cluster) from DB/price source, calls decide().
    Read-only — safe to call repeatedly (e.g. for /status what-if queries)."""
```

Orchestrator sequence: **validate keys** (`crop in CROPS`,
`region in REGION_TO_PROVINCE` — unknown key ⇒ no insert, no match, return
`hold` with an honest reason) → insert report (harvest_date = today +
days_to_harvest) → count cluster **including the new report** (crowded = ≥3
including this one) → get_recommendation → if "sell", create pending
MatchRequest → return the dict. The duplicate-report guard (same
farmer+crop+region within the window → upsert, don't double-create matches)
also lives here and nowhere else.

### Vocabulary & input normalization

The canonical vocabulary lives in **one place** — `core/models.py` (Developer A):

```python
CROPS = {"cabai_rawit_merah"}  # real Bank Indonesia commodity (see data/seed.py)
REGION_TO_PROVINCE = {"garut": "jawa_barat"}   # its keys ARE the valid regions
```

Translating farmer free text into these keys is the **adapter's** job
(Developer B), via a normalization ladder — each tier falls through to the next:

1. **Button tap** (Telegram reply keyboard) — input is already canonical; the
   bot should ask with buttons, not open questions. Buttons can't be malformed.
2. **Alias dict** — "cabe", "lombok" → `cabai_merah`; instant, free.
3. **LLM parse** (toggle: `LLM_PARSE=on|off` env var, alongside `PRICE_SOURCE`)
   — a Gemini Flash-class call acting as a **constrained classifier**: prompt
   contains the exact canonical lists, response must be one of those keys or
   `"unknown"`. Hard ~3 s timeout; timeout / error / `"unknown"` ⇒ tier 4.
   `off` skips this tier entirely — the bot stays fully functional on 1/2/4.
4. **Re-prompt with buttons** — the unconditional safety net; the experience
   degrades from "smart" to "polite," never to broken.

Strict at the boundary, trusting inside: whatever tier produced the key,
`process_harvest_report()` validates it against the constants anyway (LLM
output is untrusted adapter input), and past that gate the core functions
assume canonical keys. No LLM call exists anywhere in `/core`.

- `crop`: normalized lowercase key, e.g. `"cabai_merah"`, `"bawang_merah"`.
- `region`: normalized lowercase **district (kecamatan/kabupaten) key**, e.g.
  `"garut"` — NOT the province. Two geographies, deliberately separated:
  **clustering runs on the district** (oversupply is local — farmers in one
  district sell into the same market), while **price lookup runs on the
  province** via `REGION_TO_PROVINCE` in `core/models.py`
  (e.g. `{"garut": "jawa_barat"}`), because PIHPS surveys at province level.
  The join is one line inside `get_recommendation()`: cluster on `region`,
  fetch prices on `REGION_TO_PROVINCE[region]`. Adding a region = one mapping
  row + loading that province's price history. Never blur the two meanings.
- `reason`: human-readable string (English internally; Developer B renders Bahasa Indonesia — the bot formats from the `recommendation` code, not by parsing `reason`).

### Data shapes

*(The original CLAUDE.md "section 4" defining these was lost; the shapes below are the working definition — change them only by agreement between both devs.)*

**HarvestReport**
```json
{
  "id": 1,
  "farmer_id": 3,
  "crop": "cabai_merah",
  "region": "jawa_barat",
  "harvest_date": "2026-07-20",
  "quantity_kg": 150,
  "created_at": "2026-07-16T09:30:00"
}
```

**PriceSnapshot**
```json
{
  "crop": "cabai_merah",
  "region": "jawa_barat",
  "date": "2026-07-15",
  "price_idr_per_kg": 42000
}
```

**MatchRequest**
```json
{
  "id": 1,
  "harvest_report_id": 1,
  "buyer_id": 1,
  "status": "pending",
  "created_at": "2026-07-16T09:30:05"
}
```
`status` ∈ `pending | confirmed | declined`.

**Recommendation output**
```json
{ "recommendation": "sell", "reason": "Price falling and 4 nearby farmers harvesting within 2 days — sell before local oversupply." }
```

---

## 3. Data model (SQLite)

Single-file SQLite DB (`panen.db`), initialized by `core/db.py`.

```sql
CREATE TABLE farmer (
    id          INTEGER PRIMARY KEY,
    telegram_id TEXT UNIQUE,
    name        TEXT,
    region      TEXT NOT NULL
);

CREATE TABLE harvest_report (
    id           INTEGER PRIMARY KEY,
    farmer_id    INTEGER NOT NULL REFERENCES farmer(id),
    crop         TEXT NOT NULL,
    region       TEXT NOT NULL,
    harvest_date TEXT NOT NULL,          -- ISO date
    quantity_kg  REAL,
    created_at   TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE price_snapshot (
    id               INTEGER PRIMARY KEY,
    crop             TEXT NOT NULL,
    region           TEXT NOT NULL,
    date             TEXT NOT NULL,      -- ISO date
    price_idr_per_kg INTEGER NOT NULL,
    UNIQUE (crop, region, date)
);

CREATE TABLE match_request (
    id                INTEGER PRIMARY KEY,
    harvest_report_id INTEGER NOT NULL REFERENCES harvest_report(id),
    buyer_id          INTEGER NOT NULL DEFAULT 1,   -- single anchor buyer for demo
    status            TEXT NOT NULL DEFAULT 'pending'
                      CHECK (status IN ('pending','confirmed','declined')),
    created_at        TEXT NOT NULL DEFAULT (datetime('now'))
);
```

Notes:
- Dates stored as ISO-8601 text — SQLite's native comparison works and it keeps seeding trivial.
- `price_snapshot` rows are loaded from `data/price_cache.json`; the JSON is the source of truth for price history, the table is just its queryable form.
- One anchor buyer for the demo; `buyer_id` is a column so multi-buyer is a schema-free upgrade later.

---

## 4. Core logic pipeline (Developer A)

Flow when a farmer submits a report:

```
HarvestReport (new)
      │
      ├──► clustering.count_cluster(crop, region, harvest_date)
      │        # COUNT(*) of harvest_reports with same crop+region
      │        # and harvest_date within ±2 days of the new report
      │
      ├──► price_trend.get_trend(crop, region)
      │        # prices come from the active PriceSource (cache or live PIHPS);
      │        # windows are anchored to the LATEST DATE IN THE DATA, never
      │        # date.today(): mean of last 3 data-days vs. mean of the 4
      │        # data-days before that; >+5% = rising, <-5% = falling, else flat.
      │        # Also returns the latest data date so the bot can show
      │        # "harga per <tanggal>" honestly.
      │
      └──► rules.get_recommendation(crop, region, days_to_harvest)
               # combines cluster_size + trend per rule table (§5)
               │
               └── if "sell" ──► matching.create_match_request(report_id)
                                      # status = 'pending', visible to buyer bot
```

Each stage is a pure-ish function taking primitives and a DB connection — independently testable from a REPL with no Telegram anywhere in sight.

### Price data: fallback chain (`data/sources.py`, `data/loader.py`)

Price sources form an ordered **fallback chain** behind one interface. Each source is
tried in order with a hard timeout; the first one that returns usable data wins. The
last link (cache) cannot fail, so the demo cannot crash.

```python
class PriceSource(Protocol):
    name: str
    def get_prices(self, crop: str, province: str) -> list[PriceSnapshot]: ...
        # province-level key (see §2 region note)
        # raises SourceUnavailable on timeout / HTTP error / bad payload

class PIHPSSource:       # 1. Bank Indonesia PIHPS (bi.go.id/hargapangan) — live
class PanelHargaSource:  # 2. Badan Pangan Panel Harga (panelharga.badanpangan.go.id) — live
class CachedSource:      # 3. data/price_cache.json — never fails, terminal fallback

class ChainedSource:     # walks the chain, returns (prices, source_name)
    def __init__(self, sources: list[PriceSource]): ...
```

**The chain (live mode):** `PIHPS → PanelHarga → Cache`

1. **`PIHPSSource`** — Bank Indonesia PIHPS. No official API; the price table loads
   via XHR endpoints discoverable in browser DevTools (`GetGridData`-style POST
   returning JSON). ~5 s timeout.
2. **`PanelHargaSource`** — Badan Pangan's Panel Harga, an independent government
   source with different infrastructure (it has its own JSON XHR endpoints behind
   panelharga.badanpangan.go.id). Different commodity/region IDs than PIHPS, so it
   needs its own small mapping table. ~5 s timeout. Note: prices differ slightly
   between the two sources — that's fine; the trend function only compares a source
   against *itself* (never mix rows from different sources in one trend window).
3. **`CachedSource`** — reads `data/price_cache.json` keyed by `"{crop}|{province}"`
   (price data is province-level — see the §2 region note)
   → list of `{date, price_idr_per_kg}`. Zero network. This is what the seeded demo
   scenarios and unit tests run against, and the terminal fallback in live mode.

**Chain rules:**
- **Live sources fetch a range, not a day** — request the last 7 days in one call
  (PIHPS/Panel Harga table endpoints take date ranges), so a single live call
  returns a trend-ready series.
- **A source's series = fresh live rows ∪ that source's cached rows.** Same-source
  merging is required; *cross*-source mixing in one trend window is what's
  forbidden (survey methodologies differ — a source switch would look like a
  price movement).
- **Minimum-data rule:** if a source can't produce ≥5 distinct data days after
  merging, it raises `SourceUnavailable` for that query and the chain moves on.
  `loader.py` pre-populates the cache with 7+ days before the demo, so
  `get_trend()` never sees a series it can't compute honestly.
- Every result is tagged with `source_name` (`"pihps"` / `"panelharga"` / `"cache"`)
  so the bot can honestly say where the price came from — *"harga langsung dari
  PIHPS"*, *"harga dari Panel Harga Badan Pangan"*, or *"harga tersimpan"*. A live
  fetch is a demo highlight; a fallback is transparent, never faked.
- On any live success, **write-through**: merge fresh rows into `price_cache.json`
  (kept per-source: `"{crop}|{province}|{source}"` internally, flattened for the
  cache fallback) so the cache is never staler than the last good live call.
- Per-source failures are logged but silent to the farmer — the chain just moves on.

**Mode selection:** `PRICE_SOURCE=live|cache` env var sets the default chain
(`live` = full chain, `cache` = cache only, used by tests and as the pre-demo safe
default), plus an optional coordinator-only bot command (`/live on|off`) to flip it
on stage. `get_recommendation()` never knows which source answered — it just
receives price rows.

**Verified risk (2026-07-16):** Panel Harga was down for maintenance while PIHPS was
up — on another day it could be the reverse. That's exactly why the chain has two
independent live sources before the cache. Rehearse three ways: full live, PIHPS
blocked (forces source #2), and network off (forces cache).

### Rule engine (`core/rules.py`)

*(The original "section 5" rule table was also lost; this is the working table — same rule as above: change only by agreement.)*

Cluster threshold: **≥ 3** reports (including this one) with same crop+region within ±2 days ⇒ "crowded."

| Price trend | Cluster crowded? | Recommendation | Rationale |
|-------------|------------------|----------------|-----------|
| falling     | yes              | **sell**       | Price dropping AND local glut coming — sell now via anchor buyer before it gets worse |
| falling     | no               | **sell**       | Price dropping — don't wait for it to fall further |
| flat        | yes              | **sell**       | Oversupply will push the local price down even if the market is flat |
| flat        | no               | **hold**       | No pressure either way — sell on your normal schedule |
| rising      | yes              | **hold**       | Price rising but many neighbors selling — wait a little, but not long |
| rising      | no               | **wait**       | Price rising and no glut — waiting a few days likely pays off |

`days_to_harvest` acts as an override: if `days_to_harvest <= 1`, the crop can't wait — `wait` downgrades to `hold`, and `hold` with a falling trend becomes `sell`.

Every branch fills `reason` with the specific numbers used (cluster count, % price change) so the bot's message is credible, not generic.

---

## 5. Demo scenarios (seed fixtures)

`data/seed.py` inserts three predictable scenarios so Developer B can build conversations against known outputs:

| Scenario   | Seeded state                                             | Expected output |
|------------|----------------------------------------------------------|-----------------|
| Oversupply | 4 reports, same crop+region, harvest dates within 2 days; falling price series | `sell` + MatchRequest created |
| Scarcity   | 0 other reports; rising price series                     | `wait` |
| Neutral    | 1 other report; flat price series                        | `hold` |

**Time rules (prevents demo-day date rot):**
- Seeds contain **no literal dates** — everything is computed relative to
  `date.today()` at seed time (harvest dates = `today + 2`, price series =
  `today - 7 … today - 1`). Re-seeding an hour before the demo guarantees fresh
  scenarios.
- `date.today()` is called **only at entry points** (`process_harvest_report`
  takes `today: date | None = None`) and threaded through — never deep inside
  logic. Tests pass a frozen date and are fully deterministic.
- The trend function is anchored to the latest date in the price data (see §4),
  so it tolerates stale caches regardless.

Seeding is idempotent (wipes and re-inserts) so the demo can be reset in one command: `python -m data.seed`.

---

## 6. Telegram adapter (Developer B) — boundary view only

Developer A does not need the internals; what matters architecturally:

- The bot is a **thin adapter**: it collects `(crop, region, days_to_harvest)` from a conversation, calls `get_recommendation()`, and renders the result in Bahasa Indonesia. No business rules live in the bot.
- Until merge, the bot uses a mock with the exact same signature — the swap is a one-line import change.
- Buyer flow reads `match_request WHERE status='pending'` and updates `status`; that's the only write the adapter performs on core tables besides inserting `harvest_report` rows and farmer registration.
- `/status` is a read-only listing of pending matches for the coordinator.

---

## 7. Testing & demo readiness

- `tests/test_rules.py` runs the rule engine against all three seeded scenarios plus edge cases (`days_to_harvest = 0`, unknown crop/region → safe default `hold` with an honest reason, empty price history → `flat`).
- Rule engine must be demoable from a plain script/REPL **before** any bot exists — this is Developer A's independent milestone.
- Merge checklist: swap mock → real, run all 3 scenarios end-to-end through Telegram, freeze code hours before the demo.

## 8. Deliberate non-goals (for the demo)

- No hard dependency on live PIHPS — live mode is a best-effort showcase; the cache
  is always the safety net and the only thing tests rely on.
- No multi-buyer matching logic (single anchor buyer).
- No auth beyond Telegram identity.
- No web dashboard — `/status` command suffices.
