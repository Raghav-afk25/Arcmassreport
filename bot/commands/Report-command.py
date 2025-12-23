import json
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

# In-memory storage for frozen IDs
# For persistence, this can be replaced with a database or file system
frozen_ids = set()

# Load frozen IDs on bot startup (if persistence is implemented via file storage)
try:
    with open("frozen_ids.json", "r") as file:
        frozen_ids = set(json.load(file))
except FileNotFoundError:
    pass

# Save frozen IDs to file (if persistence is required)
def save_frozen_ids():
    with open("frozen_ids.json", "w") as file:
        json.dump(list(frozen_ids), file)

# Command: /report
# Functionality to track and freeze reported IDs
def report_command(update: Update, context: CallbackContext):
    if context.args:
        reported_id = context.args[0]
        
        if reported_id in frozen_ids:
            update.message.reply_text(f"ID {reported_id} is already frozen and cannot be reported again.")
        else:
            frozen_ids.add(reported_id)
            save_frozen_ids()  # Save changes to persistent storage
            update.message.reply_text(f"ID {reported_id} has been reported and is now frozen.")
    else:
        update.message.reply_text("Usage: /report <ID>")

# Add the command handler to your updater or application
report_handler = CommandHandler("report", report_command)
# Example: updater.dispatcher.add_handler(report_handler)
