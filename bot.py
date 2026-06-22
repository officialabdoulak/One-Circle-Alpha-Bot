import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes



TOKEN = os.getenv("BOT_TOKEN")

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

OWNER_ID = 7351567120
SUBSCRIBERS_FILE = "subscribers.txt"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_subscriber(update.effective_user.id)

    await update.message.reply_text(
        "WELCOME TO ONE CIRCLE ALPHA\n\n"
        "Your private hub for updates, alpha, and opportunities.\n\n"
        "Type /commands to view all available commands.\n\n"
        "Stay focused.\n"
        "Stay early.\n"
        "Stay ahead."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - Welcome message\n"
        "/help - List all commands\n"
        "/about - About One Circle Alpha\n"
        "/links - Important community links\n"
        "/myid - Show your Telegram ID\n"
        "/commands - Full list of commands with explanations"
    )

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


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        " ONE CIRCLE ALPHA\n\n"
        "One Circle Alpha is your private hub for updates, alpha, and opportunities.\n\n"
        "Stay focused.\n"
        "Stay early.\n"
        "Stay ahead."
    )


async def links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔗 IMPORTANT LINKS\n\n"
        "🐦 X: https: Coming Soon\n"
        "💬 Telegram: Coming Soon\n"
        "🌐 Website: Coming Soon"
    )


async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    await update.message.reply_text(
        f"🆔 Your Telegram ID:\n\n{user_id}"
    )


async def commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ONE CIRCLE ALPHA COMMANDS\n\n"

        "/start\n"
        "Welcome message.\n\n"

        "/help\n"
        "List all commands.\n\n"

        "/about\n"
        "About One Circle Alpha.\n\n"

        "/links\n"
        "Important community links.\n\n"

        "/myid\n"
        "Show your Telegram ID.\n\n"

        "/commands\n"
        "Full list of commands with explanations."
    )


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("about", about))
app.add_handler(CommandHandler("links", links))
app.add_handler(CommandHandler("myid", myid))
app.add_handler(CommandHandler("commands", commands))
app.add_handler(CommandHandler("broadcast", broadcast))

print("One Circle Alpha Bot is running...")

app.run_polling()