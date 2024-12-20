import os

from typing import Final

from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from telegram.error import Conflict

from bot.handlers.commands import start, book

# Constants
TOKEN: Final = os.environ.get("TOKEN")
BOT_USERNAME: Final = os.environ.get("BOT_USERNAME")

# Application Setup (Using ApplicationBuilder class)
def main() -> None:
    # application = ApplicationBuilder().token(TOKEN).build()
    
    # # Commands and Callback query handlers
    # application.add_handler(CommandHandler("start", start))
    # application.add_handler(CommandHandler("book", book))
    # # application.add_handler(CallbackQueryHandler(salon_selection))
    # # application.add_handler(CallbackQueryHandler(confirm_appointment))
    
    # # Start polling for updates
    # try:
    #     application.run_polling()
    # except Conflict:
    #     print("Another instance of the bot is running, Exiting.")
    #     application.stop()
    pass