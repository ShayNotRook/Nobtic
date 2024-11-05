from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from .handlers.commands import start, book


# Application Setup (Using ApplicationBuilder class)
def main() -> None:
    application = ApplicationBuilder().token("7887786324:AAHeLL7-W7goUT45ftDgqwL4dt5773h1euc").build()
    
    # Commands and Callback query handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("book", book))
    application.add_handler(CallbackQueryHandler(salon_selection))
    application.add_handler(CallbackQueryHandler(confirm_appointment))
    
    # Start polling for updates
    application.run_polling()