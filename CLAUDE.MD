# Panen Pas — Two-Developer Parallel Roadmap

Goal: split work so both developers can build independently against an agreed contract, then merge without untangling each other's code the night before the demo.

**The merge contract (agree on this FIRST, before either dev writes code):**
- The exact JSON/dict shape of a `HarvestReport`, `PriceSnapshot`, and the recommendation output (see CLAUDE.md section 4).
- The function signature: `get_recommendation(crop: str, region: str, days_to_harvest: int) -> {recommendation: str, reason: str}`.
- Both devs build against this contract using mock data until it's time to wire the real pieces together. This is what lets you work in parallel without blocking each other.

---

## Developer A — Data & Logic Track

**Owns:** everything in `/core` and `/data`. Nothing Telegram-specific.

### Roadmap
1. **Set up SQLite schema** for Farmer, HarvestReport, PriceSnapshot, MatchRequest.
2. **Build the PIHPS price data loader** — manually export or scrape recent chili/shallot price history for your chosen region; cache it as `/data/price_cache.json`. Confirm this works and looks reasonable before building anything on top.
3. **Write the cluster-detection function** — given a new HarvestReport, count how many existing reports match crop+region within a ±2 day window.
4. **Write the price-trend function** — given crop+region, return rising/flat/falling from the cached price data.
5. **Write the rule engine** (`get_recommendation()`) combining both signals per the rule table in CLAUDE.md section 5.
6. **Write the buyer-match creator** — when recommendation is "sell," create a MatchRequest record with status `pending`.
7. **Seed the three demo scenarios** (oversupply / scarcity / neutral) as test fixtures so Developer B can build the bot conversation against real, predictable outputs.
8. **Unit test the rule engine directly** (no Telegram involved) — this should be fully testable and demoable via a plain Python script or REPL before any bot exists.

**Deliverable at merge time:** a working `get_recommendation()` function and a seeded database Developer B can call into.

---

## Developer B — Bot & Interface Track

**Owns:** everything in `/adapters/telegram`. Nothing about price data or the rule engine internals.

### Roadmap
1. **Set up the Telegram bot** via BotFather, get a token, confirm `python-telegram-bot` receives messages via long polling (use a placeholder "echo" reply first — don't wait on Developer A to test this).
2. **Build the farmer conversation flow** — ask crop, ask days-to-harvest, confirm back what was understood. Use mock/hardcoded recommendation responses while Developer A's engine isn't ready yet.
3. **Build the recommendation reply formatting** — turn `{recommendation: str, reason: str}` into a clear, friendly Bahasa Indonesia message.
4. **Build the buyer-side chat flow** — a second bot conversation (or a separate command in the same bot) where the anchor buyer sees a pending match and can confirm/decline.
5. **Build the coordinator view** — even a simple `/status` command listing pending matches is enough; a full dashboard is not required for the demo.
6. **Once Developer A's `get_recommendation()` is ready, swap the mock call for the real one** — this should be a one-line change if the contract was followed.
7. **Rehearse the live demo flow end-to-end**, including what happens if a message is malformed (farmer types something the bot doesn't expect) — handle gracefully, don't crash on stage.

**Deliverable at merge time:** a working Telegram bot that farmers and the anchor buyer can both interact with, calling into the real rule engine.

---

## Merge point (do this together, not solo)

1. Developer B swaps mock recommendation calls for Developer A's real `get_recommendation()` function.
2. Run all three seeded demo scenarios end-to-end through the actual Telegram bot — confirm each produces the expected recommendation and buyer match.
3. Freeze the code at least a few hours before presenting. Do not add features after the merge — only fix bugs found while rehearsing.

## Suggested split of remaining time
- ~40% Developer A: data + rule engine
- ~40% Developer B: bot + conversation flow
- ~20% both: merge, end-to-end testing, demo rehearsal