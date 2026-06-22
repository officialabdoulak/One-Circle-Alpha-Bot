import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler

TOKEN = os.getenv("BOT_TOKEN")

OWNER_ID = 7351567120
SUBSCRIBERS_FILE = "subscribers.txt"


def load_subscribers():
    try:
        with open(SUBSCRIBERS_FILE, "r") as file:
            return list(set(line.strip() for line in file if line.strip()))
    except FileNotFoundError:
        return []


def save_subscriber(user_id):
    subscribers = load_subscribers()

    if str(user_id) not in subscribers:
        with open(SUBSCRIBERS_FILE, "a") as file:
            file.write(str(user_id) + "\n")


def get_crypto_price(coin_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    return data[coin_id]["usd"]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_subscriber(update.effective_user.id)

    keyboard = [
        [
            InlineKeyboardButton("BTC Price", callback_data="btc"),
            InlineKeyboardButton("ETH Price", callback_data="eth")
        ],
        [
            InlineKeyboardButton("Commands", callback_data="commands"),
            InlineKeyboardButton("Links", callback_data="links")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "WELCOME TO ONE CIRCLE ALPHA\n\n"
        "Your private hub for updates, alpha, prices, and opportunities.\n\n"
        "Use the buttons below or type /commands.\n\n"
        "Stay focused.\n"
        "Stay early.\n"
        "Stay ahead.",
        reply_markup=reply_markup
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - Welcome message\n"
        "/help - List all commands\n"
        "/about - About One Circle Alpha\n"
        "/links - Important community links\n"
        "/myid - Show your Telegram ID\n"
        "/commands - Full list of commands\n"
        "/btc - Check BTC price\n"
        "/eth - Check ETH price\n"
        "/users - Admin only\n"
        "/broadcast - Admin only"
    )


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ONE CIRCLE ALPHA\n\n"
        "One Circle Alpha is your private hub for updates, alpha, and opportunities.\n\n"
        "Stay focused.\n"
        "Stay early.\n"
        "Stay ahead."
    )


async def links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "IMPORTANT LINKS\n\n"
        "X: Coming Soon\n"
        "Telegram: Coming Soon\n"
        "Website: Coming Soon"
    )


async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await update.message.reply_text(f"Your Telegram ID:\n\n{user_id}")


async def commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ONE CIRCLE ALPHA COMMANDS\n\n"
        "/start\nWelcome message.\n\n"
        "/help\nList all commands.\n\n"
        "/about\nAbout One Circle Alpha.\n\n"
        "/links\nImportant community links.\n\n"
        "/myid\nShow your Telegram ID.\n\n"
        "/btc\nCheck BTC price.\n\n"
        "/eth\nCheck ETH price.\n\n"
        "/commands\nFull list of commands with explanations."
    )


async def btc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price = get_crypto_price("bitcoin")
    await update.message.reply_text(f"BTC Price: ${price}")


async def eth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price = get_crypto_price("ethereum")
    await update.message.reply_text(f"ETH Price: ${price}")


async def users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return

    subscribers = load_subscribers()
    await update.message.reply_text(f"Total subscribers: {len(subscribers)}")


async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return

    message = " ".join(context.args)

    if not message:
        await update.message.reply_text("Use: /broadcast your message")
        return

    subscribers = load_subscribers()
    sent = 0

    for user_id in subscribers:
        try:
            await context.bot.send_message(chat_id=int(user_id), text=message)
            sent += 1
        except:
            pass

    await update.message.reply_text(f"Broadcast sent to {sent} users.")


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "btc":
        price = get_crypto_price("bitcoin")
        await query.message.reply_text(f"BTC Price: ${price}")

    elif query.data == "eth":
        price = get_crypto_price("ethereum")
        await query.message.reply_text(f"ETH Price: ${price}")

    elif query.data == "commands":
        await query.message.reply_text(
            "/start - Welcome message\n"
            "/btc - Check BTC price\n"
            "/eth - Check ETH price\n"
            "/links - Important links\n"
            "/commands - Full command list"
        )

    elif query.data == "links":
        await query.message.reply_text(
            "IMPORTANT LINKS\n\n"
            "X: Coming Soon\n"
            "Telegram: Coming Soon\n"
            "Website: Coming Soon"
        )


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("about", about))
app.add_handler(CommandHandler("links", links))
app.add_handler(CommandHandler("myid", myid))
app.add_handler(CommandHandler("commands", commands))
app.add_handler(CommandHandler("btc", btc))
app.add_handler(CommandHandler("eth", eth))
app.add_handler(CommandHandler("users", users))
app.add_handler(CommandHandler("broadcast", broadcast))
app.add_handler(CallbackQueryHandler(button_handler))

print("One Circle Alpha Bot is running...")
app.run_polling()