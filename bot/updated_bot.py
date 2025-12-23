"""
This file contains the updated bot logic for the Arc-reporter, including the /session command
and automated reporting functionality.

Feature 1: /session Command
- Allows users to create user sessions.
- Enforces a limit of 50 sessions per user.

Feature 2: Automated Reporting
- Automatically sends reported content to Telegram via session IDs.
"""

from collections import defaultdict
from telegram import Bot, Update
from telegram.ext import CommandHandler, CallbackContext, Updater

# Initialize Telegram Bot with Token
TELEGRAM_BOT_TOKEN = 'your-telegram-bot-token-here'
TELEGRAM_CHAT_ID = 'your-telegram-chat-id-here'
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# User sessions storage (simple dictionary for demonstration; replace with persistent storage)
user_sessions = defaultdict(list)
SESSION_LIMIT = 50

def add_session(update: Update, context: CallbackContext):
    """Handler for /session command to add a session."""
    user_id = update.effective_user.id
    if len(user_sessions[user_id]) >= SESSION_LIMIT:
        update.message.reply_text("Session limit reached! Maximum 50 sessions allowed.")
        return

    if len(context.args) != 1:
        update.message.reply_text("Usage: /session <session_name>")
        return

    session_name = context.args[0]
    user_sessions[user_id].append(session_name)
    update.message.reply_text(f"Session '{session_name}' added! Total sessions: {len(user_sessions[user_id])}")

def report_content(update: Update, context: CallbackContext):
    """Handler for user-reported content. Automatically processes and sends to Telegram."""
    user_id = update.effective_user.id

    if user_id not in user_sessions or not user_sessions[user_id]:
        update.message.reply_text("No active sessions. Use /session to add a session first.")
        return

    content = " ".join(context.args)
    if not content:
        update.message.reply_text("Please provide content to report.")
        return

    # Automatically send content to Telegram per session ID
    for session in user_sessions[user_id]:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=f"Session: {session}\nUser: {user_id}\nContent: {content}")

    update.message.reply_text(f"Content reported successfully via {len(user_sessions[user_id])} sessions!")

# Main function to integrate bot handlers
def main():
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("session", add_session))
    dispatcher.add_handler(CommandHandler("report", report_content))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
