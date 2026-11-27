import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN", "9288515298:AAGCsf8IsNbAOXaWA0T82rjIwJ8QyvIPIXw")
QR_IMAGE_PATH = "qr.png"
PORT = int(os.environ.get("PORT", 8080))

# --- EDIT YOUR DETAILS HERE (IN ENGLISH) ---
BOT_NAME = "Official Bot"
SUPPORT_CONTACT = "@sellerf0ry0u"

# Set user balances by Telegram User ID: {user_id: amount}
USER_BALANCES = {
    # 123456789: 500,
}

# Telegram accounts options: (command_name, display_label, price_text, price_inr, stock)
TG_ACCOUNTS = [
    ("tg1", "🇮🇳 India", "$0.56 (₹80)", 80, 124),
    ("tg2", "🇮🇳 india-spam-acc", "$0.18 (₹30)", 30, 85),
    ("tg3", "🇮🇳 indian-old-2018", "$2.81 (₹350)", 350, 14),
    ("tg4", "🇮🇳 indian-old-2020", "$1.12 (₹150)", 150, 19),
    ("tg5", "🇮🇳 indian-old-2023", "$0.62 (₹90)", 90, 56),
    ("tg6", "🇮🇳 indian-old-2024", "$0.56 (₹80)", 80, 35),
    ("tg7", "🇷🇺 russia(+79)", "(₹300)", 300, 12),
]

# 26 WhatsApp countries: (command_name, display_label, price)
WA_COUNTRIES = [
    ("wa1", "🇮🇩 Indonesia", 100),
    ("wa2", "🇻🇳 Vietnam", 105),
    ("wa3", "🇵🇭 Philippines", 110),
    ("wa4", "🇮🇳 India", 115),
    ("wa5", "🇧🇩 Bangladesh", 120),
    ("wa6", "🇵🇰 Pakistan", 125),
    ("wa7", "🇲🇾 Malaysia", 130),
    ("wa8", "🇹🇭 Thailand", 135),
    ("wa9", "🇰🇪 Kenya", 140),
    ("wa10", "🇳🇬 Nigeria", 145),
    ("wa11", "🇿🇦 South Africa", 150),
    ("wa12", "🇪🇬 Egypt", 155),
    ("wa13", "🇲🇦 Morocco", 160),
    ("wa14", "🇧🇷 Brazil", 170),
    ("wa15", "🇨🇴 Colombia", 175),
    ("wa16", "🇦🇷 Argentina", 180),
    ("wa17", "🇲🇽 Mexico", 190),
    ("wa18", "🇷🇺 Russia", 200),
    ("wa19", "🇺🇦 Ukraine", 210),
    ("wa20", "🇵🇱 Poland", 220),
    ("wa21", "🇷🇴 Romania", 230),
    ("wa22", "🇹🇷 Turkey", 240),
    ("wa23", "🇬🇧 United Kingdom", 260),
    ("wa24", "🇨🇦 Canada", 275),
    ("wa25", "🇺🇸 United States", 290),
    ("wa26", "🇩🇪 Germany", 300),
]

ALL_COMMANDS_TEXT = (
    "/start - Start the bot and view all commands\n"
    "/help - Show all commands\n"
    "/info - About this bot\n"
    "/support - Contact support\n"
    "/telegramaccounts - Browse available Telegram accounts\n"
    "/watsappnumber - View WhatsApp SMS numbers\n"
    "/deposit - Choose your deposit option\n"
    "/1upi - Pay via UPI QR code\n"
    "/myprofile - View your profile details\n"
    "/howtouse - Learn how to use the bot\n"
    "/balance - Check your current balance"
)

web_app = Flask(__name__)


@web_app.route("/")
def home():
    return "Bot is alive!"


def run_web_server():
    web_app.run(host="0.0.0.0", port=PORT)


async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Welcome to {BOT_NAME}!\n\n"
        "Here are all available bot commands:\n"
        f"{ALL_COMMANDS_TEXT}"
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Available Commands:\n"
        f"{ALL_COMMANDS_TEXT}"
    )


async def info_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "About This Bot:\n"
        f"{BOT_NAME} is a genuine and trusted bot that provides all services reliably.\n"
        f"For assistance, contact {SUPPORT_CONTACT}."
    )


async def support_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Support:\n"
        f"For help and support, contact: {SUPPORT_CONTACT}"
    )


async def telegram_accounts_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lines = [
        "🟢 Select a Country You Need",
        "🎁 Tip: Deposit at least ₹1000 today to unlock discount.",
        "",
    ]
    for cmd, label, price_text, _price_inr, stock in TG_ACCOUNTS:
        lines.append(f"{label}: {price_text} - Stock: {stock} -> /{cmd}")

    await update.message.reply_text("\n".join(lines))


async def tg_account_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    label: str,
    price_text: str,
    price_inr: int,
    stock: int,
):
    user_id = update.effective_user.id
    bal = USER_BALANCES.get(user_id, 0)

    if bal < price_inr:
        needed = price_inr - bal
        await update.message.reply_text(
            f"Selected: {label}\n"
            f"Price: {price_text}\n"
            f"Available Stock: {stock}\n"
            f"Your Current Balance: ₹{bal}\n\n"
            f"Please deposit at least ₹{price_inr} (need ₹{needed} more) to get this account.\n"
            "Use /deposit or /1upi to pay via UPI QR code."
        )
    else:
        await update.message.reply_text(
            f"Selected: {label}\n"
            f"Price: {price_text}\n"
            f"Available Stock: {stock}\n"
            f"Your Current Balance: ₹{bal}\n\n"
            f"Please deposit ₹{price_inr} (or confirm your order) with {SUPPORT_CONTACT} to receive your account."
        )


async def watsapp_number_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lines = [
        "📲 WhatsApp SMS Numbers",
        "",
        "🟢 26 countries available",
        "📄 Page 1/3",
        "",
        "👇 Select a country to see servers (sorted by price):",
        "",
    ]
    for cmd, label, price in WA_COUNTRIES:
        lines.append(f"{label} - from ₹{price} -> /{cmd}")

    await update.message.reply_text("\n".join(lines))


async def wa_country_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, label: str, price: int):
    user_id = update.effective_user.id
    bal = USER_BALANCES.get(user_id, 0)

    if bal < price:
        needed = price - bal
        await update.message.reply_text(
            f"Selected: {label}\n"
            f"Required Price: ₹{price}\n"
            f"Your Current Balance: ₹{bal}\n\n"
            f"Please deposit at least ₹{price} (need ₹{needed} more) to get this number.\n"
            "Use /deposit or /1upi to pay via UPI QR code."
        )
    else:
        await update.message.reply_text(
            f"Selected: {label}\n"
            f"Required Price: ₹{price}\n"
            f"Your Current Balance: ₹{bal}\n\n"
            f"Please deposit ₹{price} (or confirm your order) with {SUPPORT_CONTACT} to receive your number."
        )


async def deposit_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Choose your deposit option:\n"
        "/1upi - UPI QR Code"
    )


async def one_upi_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if os.path.exists(QR_IMAGE_PATH):
        with open(QR_IMAGE_PATH, "rb") as photo:
            await update.message.reply_photo(
                photo=photo,
                caption=(
                    "Scan this UPI QR code to deposit.\n"
                    f"After payment, send your screenshot and User ID to {SUPPORT_CONTACT}."
                ),
            )
    else:
        await update.message.reply_text(
            "UPI QR code will be available soon.\n"
            f"Please contact {SUPPORT_CONTACT} for deposit assistance."
        )


async def my_profile_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = f"@{user.username}" if user.username else "Not set"
    bal = USER_BALANCES.get(user.id, 0)
    await update.message.reply_text(
        "My Profile:\n"
        f"• Name: {user.first_name}\n"
        f"• Username: {username}\n"
        f"• User ID: {user.id}\n"
        f"• Balance: ₹{bal}"
    )


async def how_to_use_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "How to Use:\n"
        "1. Check your details and User ID using /myprofile.\n"
        "2. Open /deposit and select /1upi for UPI payment.\n"
        "3. Check your balance anytime using /balance.\n"
        f"4. Reach out to {SUPPORT_CONTACT} for any assistance."
    )


async def balance_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    bal = USER_BALANCES.get(user_id, 0)
    await update.message.reply_text(
        "Balance:\n"
        f"• User ID: {user.id}\n"
        f"• Current Balance: ₹{bal}"
    )


async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text.lower()
    if "hi" in text or "hello" in text:
        await update.message.reply_text(
            f"Hello {update.effective_user.first_name}! Send /help to view all commands."
        )


def main():
    threading.Thread(target=run_web_server, daemon=True).start()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("info", info_cmd))
    app.add_handler(CommandHandler("support", support_cmd))
    app.add_handler(CommandHandler("telegramaccounts", telegram_accounts_cmd))

    for cmd, label, price_text, price_inr, stock in TG_ACCOUNTS:
        app.add_handler(
            CommandHandler(
                cmd,
                lambda update, context, lbl=label, pt=price_text, pi=price_inr, st=stock: tg_account_handler(
                    update, context, lbl, pt, pi, st
                ),
            )
        )

    app.add_handler(CommandHandler("watsappnumber", watsapp_number_cmd))

    for cmd, label, price in WA_COUNTRIES:
        app.add_handler(
            CommandHandler(
                cmd,
                lambda update, context, lbl=label, prc=price: wa_country_handler(update, context, lbl, prc),
            )
        )

    app.add_handler(CommandHandler("deposit", deposit_cmd))
    app.add_handler(CommandHandler("1upi", one_upi_cmd))
    app.add_handler(CommandHandler("myprofile", my_profile_cmd))
    app.add_handler(CommandHandler("howtouse", how_to_use_cmd))
    app.add_handler(CommandHandler("balance", balance_cmd))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
