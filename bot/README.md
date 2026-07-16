# Farmer–Buyer Matching Bot (Demo Build)

## 1. Set up the bot via BotFather

1. In Telegram, message **@BotFather** → `/newbot` → follow the prompts.
2. Copy the token it gives you (looks like `123456789:AAExxxxxxxxxxxxxxxxxxxxxxxxxx`).
3. Install deps and export the token:

   ```bash
   pip install -r requirements.txt
   export BOT_TOKEN="paste-your-token-here"
   ```
4. Sanity-check long polling works *before* building anything else:

   ```bash
   python -c "
   import os, logging
   from telegram.ext import Application, MessageHandler, filters
   logging.basicConfig(level=logging.INFO)

   async def echo(update, context):
       await update.message.reply_text(f'Echo: {update.message.text}')

   app = Application.builder().token(os.environ['BOT_TOKEN']).build()
   app.add_handler(MessageHandler(filters.TEXT, echo))
   app.run_polling()
   "
   ```
   Message your bot in Telegram — if it echoes back, polling works. This
   doesn't depend on Developer A at all, so do it first.

## 2. Set the anchor buyer's chat id

The buyer needs their own chat id so the bot can push match notifications
to them.

- Easiest way: have the buyer message the bot once, then temporarily log
  `update.effective_chat.id` (or use `@userinfobot`) to find it.

```bash
export BUYER_CHAT_ID="123456789"
```

## 3. Run the real bot

```bash
python bot.py
```

- Farmer flow: any user messages `/start`, answers crop + days, confirms,
  gets a recommendation, and the buyer is notified automatically.
- Buyer flow: the buyer taps **Terima**/**Tolak** on the notification.
- Coordinator view: anyone (for the demo — restrict later if needed) can
  run `/status` to see all matches and their state.

## 4. Swapping in Developer A's real recommendation engine

`bot.py` imports the recommendation function from a single place:

```python
from recommendation_engine import get_recommendation
```

Once Developer A's real engine is ready, as long as it exposes:

```python
def get_recommendation(crop: str, days_to_harvest: int) -> dict:
    # returns {"recommendation": str, "reason": str}
```

you only need to change **one line** — either:
- point the import at Developer A's module, e.g.
  `from real_engine import get_recommendation`, or
- replace the contents of `recommendation_engine.py` with the real logic
  and keep the function name/signature identical.

No other file needs to change.

## 5. Rehearsing the demo (do this before going live)

Walk through these on stage-conditions before the real demo:

- [ ] Farmer sends `/start`, types a crop, types a number of days → gets
      a recommendation, buyer gets notified.
- [ ] Farmer types garbage instead of a number for days (e.g. "besok") →
      bot asks again instead of crashing. ✅ handled in `farmer_ask_days`.
- [ ] Farmer sends an empty message or a huge wall of text as the crop →
      bot asks again. ✅ handled in `farmer_ask_crop`.
- [ ] Buyer taps **Tolak** → farmer gets a polite decline message, match
      status updates to `declined`.
- [ ] Buyer taps **Terima** → farmer gets a confirmation message, match
      status updates to `confirmed`.
- [ ] Run `/status` mid-demo to show the coordinator view live.
- [ ] Kill network briefly / cause an exception on purpose → confirm the
      bot logs it and replies with a graceful message instead of dying
      (`error_handler` in `bot.py`).

## Notes / known simplifications for the demo

- Match storage is in-memory (`PENDING_MATCHES` dict in `bot.py`) — fine
  for a live demo, not for production (swap for a DB later).
- Single anchor buyer via `BUYER_CHAT_ID` env var — multi-buyer routing
  would need a lookup table instead of one fixed chat id.
- `/status` isn't access-restricted in this build; add a chat-id allowlist
  before using it beyond the demo.
