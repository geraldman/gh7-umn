import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

import config
from store import store
from rule_engine import get_recommendation
from formatter import (
    format_recommendation_message,
    format_buyer_match_message,
    format_coordinator_status
)

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation States
CROP, DAYS, CONFIRM = range(3)

# --- Role Selection & Welcome ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Greets the user and asks them to select their role."""
    # Ensure they start from clean state if they were in a conversation
    context.user_data.clear()
    
    keyboard = [
        [
            InlineKeyboardButton("👨‍🌾 Petani (Farmer)", callback_data="set_role:Farmer"),
            InlineKeyboardButton("🤝 Pembeli (Buyer)", callback_data="set_role:Buyer")
        ],
        [
            InlineKeyboardButton("📊 Koordinator (Coordinator)", callback_data="set_role:Coordinator")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "👋 *Selamat datang di Platform Kemitraan Tani!*\n\n"
        "Silakan pilih peran Anda untuk memulai demo ini:"
    )
    
    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")
    elif update.callback_query:
        await update.callback_query.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")
    
    return ConversationHandler.END

async def set_role_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles role selection via inline buttons."""
    query = update.callback_query
    await query.answer()
    
    # Expected format: "set_role:ROLE"
    _, role = query.data.split(":")
    user_id = query.from_user.id
    username = query.from_user.username or query.from_user.first_name
    
    store.set_user_role(user_id, username, role)
    
    if role == "Farmer":
        await query.edit_message_text(
            "👨‍🌾 *Peran Terdaftar: Petani*\n\n"
            "Mari masukkan data hasil panen Anda.\n"
            "Silakan masukkan *nama tanaman* yang Anda tanam (contoh: Padi, Cabai, Tomat):",
            parse_mode="Markdown"
        )
        # Manually transition the user to the CROP state of the conversation
        return CROP
    elif role == "Buyer":
        await query.edit_message_text(
            "🤝 *Peran Terdaftar: Pembeli Utama*\n\n"
            "Anda akan menerima notifikasi otomatis ketika ada rekomendasi kecocokan petani baru. "
            "Anda dapat langsung menerima atau menolaknya dari obrolan ini.",
            parse_mode="Markdown"
        )
        return ConversationHandler.END
    elif role == "Coordinator":
        await query.edit_message_text(
            "📊 *Peran Terdaftar: Koordinator*\n\n"
            "Anda dapat memantau seluruh status pencocokan hasil panen menggunakan perintah /status.",
            parse_mode="Markdown"
        )
        return ConversationHandler.END

    return ConversationHandler.END

# --- Farmer Conversation Flow ---
async def farmer_crop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Saves the crop name and asks for days to harvest."""
    crop = update.message.text.strip()
    if not crop:
        await update.message.reply_text("Nama tanaman tidak boleh kosong. Silakan masukkan nama tanaman:")
        return CROP
        
    context.user_data['crop'] = crop
    await update.message.reply_text(
        f"Gandum/Sayur/Buah: *{crop}*.\n\n"
        f"Berapa hari lagi tanaman tersebut siap dipanen? (Masukkan angka bulat saja, misal: 45):",
        parse_mode="Markdown"
    )
    return DAYS

async def farmer_days(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Saves days to harvest (with validation) and asks for confirmation."""
    days_text = update.message.text.strip()
    try:
        days = int(days_text)
        if days < 0:
            raise ValueError("Hari tidak boleh negatif.")
    except ValueError:
        await update.message.reply_text(
            "⚠️ *Input tidak valid!*\n"
            "Mohon masukkan angka bulat positif saja (misalnya: 30, 45, 60):",
            parse_mode="Markdown"
        )
        return DAYS

    context.user_data['days'] = days
    crop = context.user_data['crop']
    
    reply_keyboard = [["Ya", "Tidak"]]
    await update.message.reply_text(
        f"📋 *Konfirmasi Data Pertanian Anda:*\n"
        f"- Tanaman: {crop}\n"
        f"- Sisa Hari Panen: {days} hari\n\n"
        f"Apakah data di atas sudah benar?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True),
        parse_mode="Markdown"
    )
    return CONFIRM

async def farmer_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Processes confirmation, fetches recommendation, and alerts buyers."""
    answer = update.message.text.strip().lower()
    
    if answer == "tidak":
        await update.message.reply_text(
            "Baik, mari ulangi.\n"
            "Silakan masukkan kembali *nama tanaman* Anda:",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode="Markdown"
        )
        return CROP
    elif answer != "ya":
        await update.message.reply_text(
            "Mohon klik tombol *Ya* atau *Tidak* di bawah keyboard Anda.",
            parse_mode="Markdown"
        )
        return CONFIRM

    # User answered "Ya"
    crop = context.user_data['crop']
    days = context.user_data['days']
    farmer_id = update.effective_user.id
    farmer_name = update.effective_user.username or update.effective_user.first_name
    
    # 1. Call Recommendation Engine (mock or real)
    rec_data = get_recommendation(crop, days)
    
    # 2. Save Match in Local DB
    match_id = store.create_match(
        farmer_id=farmer_id,
        farmer_name=farmer_name,
        crop=crop,
        days_to_harvest=days,
        recommendation=rec_data["recommendation"],
        reason=rec_data["reason"]
    )
    
    # 3. Format and Send Recommendation to Farmer
    farmer_message = format_recommendation_message(crop, days, rec_data)
    await update.message.reply_text(
        farmer_message,
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="Markdown"
    )
    
    # 4. Notify Registered Buyers
    buyers = store.get_users_by_role("Buyer")
    if not buyers:
        await update.message.reply_text(
            "ℹ️ _Catatan: Belum ada Pembeli Utama yang terdaftar di sistem. "
            "Rekomendasi Anda tersimpan, dan akan ditampilkan di laporan status._",
            parse_mode="Markdown"
        )
    else:
        buyer_message = format_buyer_match_message(match_id, farmer_name, crop, days, rec_data)
        buyer_keyboard = [
            [
                InlineKeyboardButton("✅ Terima (Accept)", callback_data=f"buyer_match:accept:{match_id}"),
                InlineKeyboardButton("❌ Tolak (Decline)", callback_data=f"buyer_match:decline:{match_id}")
            ]
        ]
        buyer_markup = InlineKeyboardMarkup(buyer_keyboard)
        
        for buyer in buyers:
            try:
                await context.bot.send_message(
                    chat_id=buyer["user_id"],
                    text=buyer_message,
                    reply_markup=buyer_markup,
                    parse_mode="Markdown"
                )
            except Exception as e:
                logger.error(f"Failed to notify buyer {buyer['user_id']}: {e}")
                
        await update.message.reply_text(
            "🔔 Notifikasi kecocokan telah dikirimkan ke Pembeli Utama terdaftar.",
            parse_mode="Markdown"
        )

    context.user_data.clear()
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text(
        "Alur pengisian data pertanian dibatalkan. Anda dapat mengulangi dengan perintah /start.",
        reply_markup=ReplyKeyboardRemove()
    )
    context.user_data.clear()
    return ConversationHandler.END

# --- Buyer Decision Handling ---
async def buyer_decision_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processes buyer's Accept or Decline choice."""
    query = update.callback_query
    await query.answer()
    
    # Expected format: "buyer_match:ACTION:MATCH_ID"
    parts = query.data.split(":")
    if len(parts) != 3:
        return
        
    _, action, match_id = parts
    match = store.get_match(match_id)
    
    if not match:
        await query.edit_message_text("❌ Data kecocokan tidak ditemukan.")
        return
        
    if match["status"] != "Pending":
        await query.edit_message_text(
            f"ℹ️ Kecocokan ini sudah diproses sebelumnya.\n"
            f"Status saat ini: *{match['status']}*",
            parse_mode="Markdown"
        )
        return

    new_status = "Accepted" if action == "accept" else "Declined"
    store.update_match_status(match_id, new_status)
    
    # Update Buyer's message
    action_text = "Diterima ✅" if action == "accept" else "Ditolak ❌"
    await query.edit_message_text(
        query.message.text + f"\n\nKeputusan Anda: *{action_text}*",
        parse_mode="Markdown"
    )
    
    # Notify Farmer
    farmer_id = match["farmer_id"]
    crop_name = match["crop"].capitalize()
    
    if action == "accept":
        farmer_notification = (
            f"🎉 *Kabar Baik!*\n"
            f"Pembeli Utama telah *menyetujui* penawaran hasil panen Anda (ID Match: `{match_id}`).\n"
            f"Tanaman: *{crop_name}*\n"
            f"Mereka akan segera menghubungi Anda untuk koordinasi lebih lanjut."
        )
    else:
        farmer_notification = (
            f"⚠️ *Pembaruan Status Kecocokan*\n"
            f"Pembeli Utama telah *menolak* penawaran hasil panen Anda (ID Match: `{match_id}`) untuk saat ini.\n"
            f"Tanaman: *{crop_name}*\n"
            f"Tetap semangat, Anda bisa mencoba memasukkan tanaman lain."
        )
        
    try:
        await context.bot.send_message(
            chat_id=farmer_id,
            text=farmer_notification,
            parse_mode="Markdown"
        )
    except Exception as e:
        logger.error(f"Failed to notify farmer {farmer_id} about decision: {e}")

# --- Coordinator Commands ---
async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Displays all matches to registered coordinators."""
    user_id = update.effective_user.id
    role = store.get_user_role(user_id)
    
    if role != "Coordinator":
        await update.message.reply_text(
            "❌ *Akses Ditolak!*\n"
            "Perintah ini hanya dapat diakses oleh pengguna dengan peran *Koordinator*.\n"
            "Ketik /start untuk mengubah peran Anda.",
            parse_mode="Markdown"
        )
        return
        
    matches = store.get_all_matches()
    status_report = format_coordinator_status(matches)
    await update.message.reply_text(status_report, parse_mode="Markdown")

# --- Main Initialization ---
def main() -> None:
    token = config.TELEGRAM_TOKEN
    if not token or token == "your_fallback_placeholder_token_here":
        print("CRITICAL ERROR: No Telegram token provided. Please configure .env file.")
        return
        
    application = Application.builder().token(token).build()

    # Conversation handler for farmers (and first-time role selection fallback)
    conv_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(set_role_callback, pattern="^set_role:"),
            CommandHandler("start", start)
        ],
        states={
            CROP: [MessageHandler(filters.TEXT & ~filters.COMMAND, farmer_crop)],
            DAYS: [MessageHandler(filters.TEXT & ~filters.COMMAND, farmer_days)],
            CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, farmer_confirm)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        per_message=False  # Keep standard conversation behavior per chat
    )

    # Register handlers
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CallbackQueryHandler(buyer_decision_callback, pattern="^buyer_match:"))
    
    # Catch-all start to make sure starting is always responsive
    application.add_handler(CommandHandler("start", start))

    print("Starting Telegram Bot long polling...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
