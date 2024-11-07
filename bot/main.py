import os
print(os.getcwd())

from typing import Final

from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler

from bot.handlers.commands import start, book

# Constants
TOKEN: Final = os.environ.get("TOKEN")
BOT_USERNAME: Final = os.environ.get("BOT_USERNAME")

# Application Setup (Using ApplicationBuilder class)
async def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Commands and Callback query handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("book", book))
    # application.add_handler(CallbackQueryHandler(salon_selection))
    # application.add_handler(CallbackQueryHandler(confirm_appointment))
    
    # Start polling for updates
    await application.run_polling()