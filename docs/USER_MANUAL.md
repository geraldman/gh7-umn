# Agria (Panen Pas) — User Manual

> **Submitted for Garuda Hacks 7 — Universitas Multimedia Nusantara.**

Agria is a Telegram bot (WhatsApp is the intended production channel) that helps
Indonesian chili farmers decide **when to sell** and connects them to an anchor
buyer — no app to download, just a chat.

The bot detects a problem no price app catches: when many farmers in the same
district harvest in the same few days, the **local** price collapses even while
the provincial price looks stable. Agria warns farmers before that glut hits and
helps a buyer aggregate the harvest efficiently.

- **Demo bot:** [@AgriaGH7_bot](https://t.me/AgriaGH7_bot) on Telegram
- **Language:** the bot's interface is in **Bahasa Indonesia**. This manual is in
  English for reference; the exact on-screen labels are shown in quotes.
- **Crop covered:** Cabai Rawit Merah (bird's-eye chili) — the most volatile
  commodity in our dataset (Bank Indonesia coefficient of variation ~32–37%).
- **Regions covered:** Garut & Cianjur (→ Jawa Barat), Brebes (→ Jawa Tengah).

---

## 1. Getting started

1. Open Telegram and search for **@AgriaGH7_bot** (or tap the link above).
2. Press **Start** or send **/start**.
3. Choose your role:
   - 👨‍🌾 **Petani** (Farmer) — report a harvest, get a sell recommendation.
   - 🏪 **Pembeli** (Buyer) — browse harvests and place buy orders.
   - 📋 **Koordinator** (Coordinator) — monitor all matches.

You can send **/start** again at any time to change your role or restart a flow,
and **/cancel** to abort whatever you're in the middle of.

---

## 2. Farmer guide (Petani)

The farmer flow is a short guided conversation. Buttons are provided at each
step, but you can also type your answer.

**Step by step:**

1. **/start → 👨‍🌾 Petani.**
2. **Choose the crop.** Tap **"Cabai Rawit Merah"**.
3. **Choose your district.** Tap **Garut**, **Cianjur**, or **Brebes**. If there
   are more than a few districts, use **⬅️ / ➡️** to page through the list.
4. **Days until harvest.** Type a whole number 0–60 (e.g. `2`).
5. **Estimated quantity (kg).** Type a number (e.g. `150`). Type `0` if unknown.
6. **Contact number.** Type your HP/WA number (e.g. `081234567890`). The buyer
   uses this to reach you.
7. **Confirm.** Review the summary and tap **"✅ Ya"** (or **"❌ Tidak"** to redo).

**If you already reported the same harvest today**, Agria asks whether the new
amount should be **added** or should **replace** the old one:

- **"➕ Tambah"** — add to your existing quantity (e.g. 100 kg + 60 kg = 160 kg).
- **"🔄 Ganti"** — replace it with the new amount.

**The recommendation.** After confirming, you receive one of three answers:

| Headline | Meaning |
|---|---|
| 🟢 **JUAL SEKARANG** | Sell now — a local glut is forming or the price is falling. |
| 🟡 **JUAL SESUAI JADWAL BIASA** | No pressure — sell on your normal schedule. |
| 🔵 **TUNGGU BEBERAPA HARI** | Wait — the price is rising and no local glut. |

Each message shows the current market price (e.g. *"Harga stabil ➖ Rp56.150/kg"*),
how many farmers nearby are harvesting at the same time, and the price date.

**When the answer is JUAL SEKARANG**, your offer is automatically sent to the
anchor buyer. If the buyer buys your stock, you'll get a notification telling you
how much sold, how much remains, and the current price.

---

## 3. Buyer guide (Pembeli)

**Setup:** **/start → 🏪 Pembeli → choose your operating region.** You are then
dropped **straight into the harvest browser** for that region (no extra command
needed).

### 3.1 Browsing harvests — `/panen`

The browser lists every harvest report in a region, grouped by crop, showing how
much stock is left:

```
📦 Laporan Panen — Garut:

🌱 Cabai Rawit Merah (4 laporan, sisa ±570 kg)
  • 120 kg, panen 2026-07-18 — Pak Asep
  • sisa 40/150 kg, panen 2026-07-19 — Bu Imas
  • 🔴 TERJUAL HABIS, panen 2026-07-19 — Pak Dedi
  • 200 kg, panen 2026-07-20 — Pak Ujang
```

- **"sisa X/Y kg"** = X kg left of an original Y kg (some already sold).
- **"🔴 TERJUAL HABIS"** = fully sold out.
- Tap another region button to switch the list in place (dropdown-style).
- Send **/panen** any time to reopen the browser.

### 3.2 Placing a buy order — 🛒 Beli

1. Tap **"🛒 Beli di <region>"**.
2. Type how many kg you want (e.g. `200`).
3. Agria proposes a **fill plan** using *Earliest-Deadline-First* allocation —
   it fills your order from the farmers whose crop will spoil soonest, combining
   partial amounts across farmers, and shows each farmer's phone number:

   ```
   🛒 Rencana pembelian di Garut — diminta 200 kg, tersedia 200 kg:
   • Ambil 90 kg dari Bu B (panen 2026-07-18, stok 90 kg) — 📞 0822...
   • Ambil 110 kg dari Pak A (panen 2026-07-19, stok 200 kg) — 📞 0811...
   ```

   If stock can't cover your order, it flags the shortfall.
4. Tap **"✅ Konfirmasi beli"** (or **"❌ Batal"**).
5. On confirmation:
   - Each farmer's remaining stock is updated (sold-out farmers get marked).
   - You receive the **contact list** to arrange pickup.
   - **Each seller is notified** that their stock sold, how much remains, and the
     current market price.

### 3.3 Match notifications

Separately, whenever a farmer's report triggers **JUAL SEKARANG**, you receive a
match card with their details and **"✅ Terima"** / **"❌ Tolak"** buttons. Either
choice notifies the farmer. *(Note: match cards and the `/panen` buy flow are two
independent channels — accepting a match card does not change `/panen` stock
figures.)*

---

## 4. Coordinator guide (Koordinator)

**/start → 📋 Koordinator**, then send **/status** to see every buyer match and
its status (⏳ menunggu / ✅ diterima / ❌ ditolak):

```
📋 Status Pencocokan:
#3 — Pak Asep: 150 kg Cabai Rawit Merah (Garut, panen 2026-07-19) — ⏳ menunggu
```

---

## 5. Administrator guide (/admin)

**Restricted.** `/admin` only works for the configured administrator
(`ADMIN_USERNAME` / `ADMIN_TELEGRAM_ID`). Everyone else sees "perintah tidak
dikenali". It is used to demonstrate live price movements.

1. Send **/admin** → pick a province (**Jawa Barat** / **Jawa Tengah**).
2. The bot shows the latest price and the "normal" band (mean ± 2σ).
3. Type a new price (e.g. `120000`). The engine reacts immediately, and:
   - **Above +2σ** → a 🚨 *spike* alert is broadcast to all users.
   - **Below −2σ** → a 🚨 *crash* alert is broadcast.
   - **Within the band** → a 📊 *stable* notice is broadcast.
4. **"♻️ Reset ke data asli (BI)"** restores the real Bank Indonesia prices
   (prices only — farmer/harvest/match data is untouched).

---

## 6. How the recommendation works

Agria combines **two signals**:

1. **Price trend** — rising / flat / falling, computed from the last 7 days of
   **real Bank Indonesia (PIHPS)** price data for the crop's province.
2. **Local harvest cluster** — how many farmers are harvesting the same crop in
   the same district within ±2 days.

Simplified rule table:

| Price trend | Local glut forming? | Recommendation |
|---|---|---|
| Falling | either | 🟢 Sell |
| Flat | yes (crowded) | 🟢 Sell — *the local glut will push the price down even though the market looks flat* |
| Flat | no | 🟡 Hold |
| Rising | yes | 🟡 Hold (briefly) |
| Rising | no | 🔵 Wait |

If the harvest is imminent (≤1 day), the advice shifts toward selling since the
crop can't wait.

---

## 7. Command reference

| Command | Who | What it does |
|---|---|---|
| `/start` | Everyone | Start / restart, choose a role |
| `/help` | Everyone | Show the command list |
| `/cancel` | Everyone | Cancel the current step |
| `/panen` | Buyer | Browse harvest reports per region and buy |
| `/status` | Coordinator | List all buyer matches |
| `/admin` | Admin only | Override price + broadcast; reset to real data |

---

## 8. Troubleshooting & FAQ

- **The bot doesn't respond.** Send **/start**. If it's still quiet, the demo
  server or database may be paused — contact the team.
- **"Komoditas itu belum didukung."** Only Cabai Rawit Merah is supported in this
  version — pick it from the button.
- **"Wilayah itu belum terdaftar."** Choose Garut, Cianjur, or Brebes from the
  buttons.
- **I entered the wrong number.** Send **/cancel** and **/start** again, or use
  the **➕ Tambah / 🔄 Ganti** prompt if you re-report the same harvest.
- **As a farmer I didn't get a "stock sold" message.** Notifications only reach
  farmers who registered through the real bot (with a real Telegram account);
  seeded demo farmers can't receive them.
- **Why is the recommendation "Sell" when the price looks stable?** That's the
  point — Agria detected that several neighbors are harvesting the same week, so
  the local price is about to drop even though the provincial price is flat.

---

## 9. About the data

Prices are **real Bank Indonesia (PIHPS) data** for Cabai Rawit Merah in Jawa
Barat and Jawa Tengah (daily history through mid-2026). Chili was chosen because
it is highly perishable (≈5-day shelf life) and highly volatile — exactly the
crop where mistimed selling costs farmers the most.

---

## 10. Submission

**Project:** Agria (Panen Pas)
**Event:** Garuda Hacks 7
**Host:** Universitas Multimedia Nusantara
