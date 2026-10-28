import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ["BOT_TOKEN"]
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")  # optional: admin's Telegram chat ID

PRODUCTS = {
    "p1": {"name": "Premium Package", "price": 100},
    "p2": {"name": "Special Package", "price": 200},
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(f'{p["name"]} — ৳{p["price"]}', callback_data=f"buy_{pid}")]
                for pid, p in PRODUCTS.items()]
    await update.effective_message.reply_text(
        "🛍️ Welcome to our store!\n\nপণ্য নির্বাচন করুন:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    pid = query.data.removeprefix("buy_")
    product = PRODUCTS.get(pid)
    if not product:
        await query.message.reply_text("পণ্যটি পাওয়া যায়নি।")
        return
    context.user_data["selected_product"] = pid
    await query.message.reply_text(
        f'আপনার পণ্য: {product["name"]}\nদাম: ৳{product["price"]}\n\n'
        "অর্ডার করতে /order লিখুন।"
    )

async def order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pid = context.user_data.get("selected_product")
    product = PRODUCTS.get(pid)
    if not product:
        await update.effective_message.reply_text("আগে /start দিয়ে পণ্য নির্বাচন করুন।")
        return

    user = update.effective_user
    order_text = (
        "🛒 নতুন অর্ডার অনুরোধ\n"
        f'পণ্য: {product["name"]}\nদাম: ৳{product["price"]}\n'
        f"ক্রেতা: {user.full_name}\nTelegram ID: {user.id}\n"
        f"Username: @{user.username}" if user.username else
        f"🛒 নতুন অর্ডার অনুরোধ\nপণ্য: {product['name']}\nদাম: ৳{product['price']}\n"
        f"ক্রেতা: {user.full_name}\nTelegram ID: {user.id}\nUsername: নেই"
    )
    await update.effective_message.reply_text(
        f'✅ অর্ডার অনুরোধ তৈরি হয়েছে!\nপণ্য: {product["name"]}\nদাম: ৳{product["price"]}\n'
        "পেমেন্ট ও ডেলিভারি নিশ্চিত করতে অ্যাডমিনের সঙ্গে যোগাযোগ করুন।"
    )
    if ADMIN_CHAT_ID:
        try:
            await context.bot.send_message(chat_id=int(ADMIN_CHAT_ID), text=order_text)
        except (ValueError, TypeError):
            await update.effective_message.reply_text("অ্যাডমিন নোটিফিকেশন সেটিং ঠিক করা নেই।")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("order", order))
app.add_handler(CallbackQueryHandler(buy, pattern=r"^buy_"))
app.run_polling()
