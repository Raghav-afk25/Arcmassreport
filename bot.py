import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Define a dictionary to store session IDs
sessions = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    session_id = sessions.get(user_id, None)

    if not session_id:
        session_id = len(sessions) + 1
        sessions[user_id] = session_id

    await update.message.reply_text(f"Welcome! Your session ID is {session_id}.")

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if user_id in sessions:
        await update.message.reply_text(f"Reporting for session ID {sessions[user_id]}.")
    else:
        await update.message.reply_text("Session not found.")


def main() -> None:
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("report", report))

    application.run_polling()
