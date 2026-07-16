"""Panen Pas Telegram bot — the adapter layer (ARCHITECTURE.md §6).

Thin by design: collects (crop, region, days, qty) via buttons, calls
core.api.process_harvest_report() — the single write path — and renders the
result in Bahasa Indonesia. No business rules live here.

Run from the repo root:  python -m bot.bot
"""
from __future__ import annotations

import logging

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from bot import config, formatter, store
from bot.nlu_extract import normalize_crop, normalize_region
from core.api import process_harvest_report
from core.models import CROPS, REGION_TO_PROVINCE

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# httpx logs every request URL — which contains the bot token. Silence it.
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# Conversation states
CROP, REGION, DAYS, QTY, CONFIRM = range(5)

# Inline keyboards (buttons attached to the message, same style as the role
# selection) — typed text still works as a fallback in every state.

def _crop_markup() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(formatter.crop_label(c), callback_data=f"crop:{c}")
        for c in sorted(CROPS)
    ]])


def _region_markup() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(formatter.region_label(r), callback_data=f"region:{r}")
        for r in sorted(REGION_TO_PROVINCE)
    ]])


def _confirm_markup() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("✅ Ya", callback_data="confirm:ya"),
        InlineKeyboardButton("❌ Tidak", callback_data="confirm:tidak"),
    ]])


# --- Role selection ------------------------------------------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    keyboard = [
        [
            InlineKeyboardButton("👨‍🌾 Petani", callback_data="set_role:Farmer"),
            InlineKeyboardButton("🏪 Pembeli", callback_data="set_role:Buyer"),
        ],
        [InlineKeyboardButton("📋 Koordinator", callback_data="set_role:Coordinator")],
    ]
    text = "👋 *Selamat datang di Panen Pas!*\n\nSilakan pilih peran Anda:"
    msg = update.message or update.callback_query.message
    await msg.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard),
                         parse_mode="Markdown")
    return ConversationHandler.END


async def set_role_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    _, role = query.data.split(":")
    user = query.from_user
    conn = store.get_connection()
    store.set_user_role(conn, user.id, user.username or user.first_name, role)

    if role == "Farmer":
        await query.edit_message_text(
            "👨‍🌾 *Peran: Petani*\n\nTanaman apa yang akan Anda panen?",
            parse_mode="Markdown",
            reply_markup=_crop_markup(),
        )
        return CROP
    if role == "Buyer":
        await query.edit_message_text(
            "🏪 *Peran: Pembeli Utama*\n\nAnda akan menerima notifikasi otomatis "
            "saat ada penawaran panen baru, dan bisa langsung menerima atau menolaknya.",
            parse_mode="Markdown",
        )
    else:
        await query.edit_message_text(
            "📋 *Peran: Koordinator*\n\nGunakan /status untuk memantau semua pencocokan.",
            parse_mode="Markdown",
        )
    return ConversationHandler.END


# --- Farmer conversation ---------------------------------------------------------

async def farmer_crop_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    crop = query.data.split(":", 1)[1]
    context.user_data["crop"] = crop
    await query.edit_message_text(
        f"🌱 {formatter.crop_label(crop)}. Di kecamatan/kabupaten mana lahan Anda?",
        reply_markup=_region_markup(),
    )
    return REGION


async def farmer_crop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    crop = normalize_crop(update.message.text)
    if crop is None:  # ladder tier 4: re-prompt with buttons, never crash
        await update.message.reply_text(
            "Maaf, komoditas itu belum didukung. Silakan pilih dari tombol:",
            reply_markup=_crop_markup(),
        )
        return CROP
    context.user_data["crop"] = crop
    await update.message.reply_text(
        f"🌱 {formatter.crop_label(crop)}. Di kecamatan/kabupaten mana lahan Anda?",
        reply_markup=_region_markup(),
    )
    return REGION


async def farmer_region_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    region = query.data.split(":", 1)[1]
    context.user_data["region"] = region
    await query.edit_message_text(
        f"📍 {formatter.region_label(region)}.\n"
        "Berapa hari lagi sampai panen? (angka saja, misal: 2)"
    )
    return DAYS


async def farmer_region(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    region = normalize_region(update.message.text)
    if region is None:
        await update.message.reply_text(
            "Wilayah itu belum terdaftar. Silakan pilih dari tombol:",
            reply_markup=_region_markup(),
        )
        return REGION
    context.user_data["region"] = region
    await update.message.reply_text(
        "Berapa hari lagi sampai panen? (angka saja, misal: 2)"
    )
    return DAYS


async def farmer_days(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        days = int(update.message.text.strip())
        if not 0 <= days <= 60:
            raise ValueError
    except ValueError:
        await update.message.reply_text(
            "⚠️ Mohon masukkan angka bulat 0–60 (misal: 2, 5, 14):"
        )
        return DAYS
    context.user_data["days"] = days
    await update.message.reply_text(
        "Perkiraan jumlah panen dalam kg? (angka saja, misal: 150 — ketik 0 jika belum tahu)"
    )
    return QTY


async def farmer_qty(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        qty = float(update.message.text.strip().replace(",", "."))
        if qty < 0:
            raise ValueError
    except ValueError:
        await update.message.reply_text("⚠️ Mohon masukkan angka saja (misal: 150):")
        return QTY
    context.user_data["qty"] = qty or None

    d = context.user_data
    await update.message.reply_text(
        f"📋 *Konfirmasi data Anda:*\n"
        f"- Komoditas: {formatter.crop_label(d['crop'])}\n"
        f"- Wilayah: {formatter.region_label(d['region'])}\n"
        f"- Panen dalam: {d['days']} hari\n"
        f"- Perkiraan: {d['qty'] or '-'} kg\n\n"
        f"Sudah benar?",
        reply_markup=_confirm_markup(),
        parse_mode="Markdown",
    )
    return CONFIRM


async def _submit_report(context, user, reply) -> int:
    """Shared by the ✅ Ya button and typed 'ya' — the actual submission."""
    d = context.user_data
    conn = store.get_connection()
    farmer_id = store.get_or_create_farmer(
        conn, user.id, user.username or user.first_name, d["region"]
    )

    # THE contract call — the adapter's only write path into core.
    result = process_harvest_report(
        farmer_id, d["crop"], d["region"], d["days"], d["qty"], conn=conn
    )

    await reply(
        formatter.format_recommendation_message(d["crop"], d["region"], d["days"], result),
        parse_mode="Markdown",
    )

    # Notify buyers only when the engine actually opened a match ("sell").
    match_id = result.get("match_request_id")
    if match_id:
        match = store.get_match(conn, match_id)
        buyers = store.get_users_by_role(conn, "Buyer")
        if buyers:
            text = formatter.format_buyer_match_message(
                match_id, match["farmer_name"], match["crop"], match["region"],
                match["harvest_date"], match["quantity_kg"],
            )
            markup = InlineKeyboardMarkup([[
                InlineKeyboardButton("✅ Terima", callback_data=f"buyer_match:accept:{match_id}"),
                InlineKeyboardButton("❌ Tolak", callback_data=f"buyer_match:decline:{match_id}"),
            ]])
            for buyer in buyers:
                try:
                    await context.bot.send_message(
                        chat_id=buyer["user_id"], text=text,
                        reply_markup=markup, parse_mode="Markdown",
                    )
                except Exception as e:
                    logger.error("Failed to notify buyer %s: %s", buyer["user_id"], e)
            await reply("📨 Penawaran Anda telah dikirim ke Pembeli Utama.")
        else:
            await reply(
                "ℹ️ _Belum ada Pembeli Utama terdaftar — penawaran Anda tersimpan "
                "dan tampil di laporan /status._", parse_mode="Markdown",
            )

    context.user_data.clear()
    return ConversationHandler.END


async def farmer_confirm_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    choice = query.data.split(":", 1)[1]
    if choice == "tidak":
        await query.edit_message_text(
            "Baik, mari ulangi. Pilih komoditas:", reply_markup=_crop_markup()
        )
        return CROP
    await query.edit_message_text(query.message.text + "\n\n✅ Dikonfirmasi.")
    return await _submit_report(context, query.from_user, query.message.reply_text)


async def farmer_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    answer = update.message.text.strip().lower()
    if answer == "tidak":
        await update.message.reply_text(
            "Baik, mari ulangi. Pilih komoditas:", reply_markup=_crop_markup()
        )
        return CROP
    if answer != "ya":
        await update.message.reply_text("Mohon jawab dengan tombol *Ya* atau *Tidak*.",
                                        parse_mode="Markdown")
        return CONFIRM
    return await _submit_report(context, update.effective_user, update.message.reply_text)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Dibatalkan. Ketik /start untuk memulai lagi.",
        reply_markup=ReplyKeyboardRemove(),
    )
    context.user_data.clear()
    return ConversationHandler.END


# --- Buyer decision ----------------------------------------------------------------

async def buyer_decision_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    parts = query.data.split(":")
    if len(parts) != 3:
        return
    _, action, match_id = parts

    conn = store.get_connection()
    match = store.get_match(conn, match_id)
    if not match:
        await query.edit_message_text("❌ Data pencocokan tidak ditemukan.")
        return
    if match["status"] != "pending":
        await query.edit_message_text(
            f"ℹ️ Pencocokan ini sudah diproses (status: {match['status']}).")
        return

    new_status = "confirmed" if action == "accept" else "declined"
    store.update_match_status(conn, match_id, new_status)
    label = "Diterima ✅" if action == "accept" else "Ditolak ❌"
    await query.edit_message_text(query.message.text + f"\n\nKeputusan Anda: {label}")

    # Never strand the farmer — every status change reaches them (judge Q7).
    crop = formatter.crop_label(match["crop"])
    if action == "accept":
        text = (f"🎉 *Kabar baik!* Pembeli Utama *menerima* penawaran "
                f"{crop} Anda (Match #{match_id}). "
                f"Mereka akan segera menghubungi Anda.")
    else:
        text = (f"ℹ️ Pembeli Utama *belum mengambil* penawaran {crop} Anda "
                f"(Match #{match_id}). Rekomendasi jual tetap berlaku — "
                f"harga pasar mendukung penjualan melalui jalur biasa Anda.")
    try:
        await context.bot.send_message(
            chat_id=int(match["farmer_telegram_id"]), text=text, parse_mode="Markdown"
        )
    except Exception as e:
        logger.error("Failed to notify farmer %s: %s", match["farmer_telegram_id"], e)


# --- Coordinator --------------------------------------------------------------------

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = store.get_connection()
    role = store.get_user_role(conn, update.effective_user.id)
    if role != "Coordinator":
        await update.message.reply_text(
            "❌ Perintah ini hanya untuk *Koordinator*. Ketik /start untuk memilih peran.",
            parse_mode="Markdown",
        )
        return
    await update.message.reply_text(
        formatter.format_coordinator_status(store.get_all_matches(conn)),
        parse_mode="Markdown",
    )


async def error_handler(update, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Update caused error: %s", context.error, exc_info=context.error)
    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text(
            "Maaf, terjadi kesalahan. Silakan coba lagi dengan /start."
        )


# --- Main -----------------------------------------------------------------------------

def main() -> None:
    if not config.TELEGRAM_TOKEN:
        print("ERROR: set the TELEGRAM_BOT_TOKEN environment variable first.")
        return

    app = Application.builder().token(config.TELEGRAM_TOKEN).build()

    conv = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(set_role_callback, pattern="^set_role:"),
            CommandHandler("start", start),
        ],
        states={
            CROP: [CallbackQueryHandler(farmer_crop_button, pattern="^crop:"),
                   MessageHandler(filters.TEXT & ~filters.COMMAND, farmer_crop)],
            REGION: [CallbackQueryHandler(farmer_region_button, pattern="^region:"),
                     MessageHandler(filters.TEXT & ~filters.COMMAND, farmer_region)],
            DAYS: [MessageHandler(filters.TEXT & ~filters.COMMAND, farmer_days)],
            QTY: [MessageHandler(filters.TEXT & ~filters.COMMAND, farmer_qty)],
            CONFIRM: [CallbackQueryHandler(farmer_confirm_button, pattern="^confirm:"),
                      MessageHandler(filters.TEXT & ~filters.COMMAND, farmer_confirm)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(conv)
    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(CallbackQueryHandler(buyer_decision_callback, pattern="^buyer_match:"))
    app.add_handler(CommandHandler("start", start))
    app.add_error_handler(error_handler)

    print("Panen Pas bot: long polling started...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
