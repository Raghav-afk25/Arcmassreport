import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Dictionary to store frozen session IDs
frozen_session_ids = set()

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Welcome to the bot! Use /report <session_id> to report content.")

def report(update: Update, context: CallbackContext) -> None:
    # Check if a session ID is provided
    if len(context.args) == 0:
        update.message.reply_text("Please provide a session ID to report.")
        return

    session_id = context.args[0]

    # Check if the session ID is already frozen
    if session_id in frozen_session_ids:
        update.message.reply_text(f"Session ID {session_id} is frozen and cannot be used again.")
        return

    # Logic for content reporting (placeholder)
    update.message.reply_text(f"Content reported with session ID: {session_id}. The session ID will now be frozen.")

    # Freeze the session ID
    frozen_session_ids.add(session_id)

def main() -> None:
    # Set up the updater and dispatcher
    updater = Updater(os.getenv("TELEGRAM_BOT_TOKEN"))
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("report", report))

    # Start polling for updates
    updater.start_polling()

    # Run the bot until you press Ctrl+C
    updater.idle()

if __name__ == "__main__":
    main()
