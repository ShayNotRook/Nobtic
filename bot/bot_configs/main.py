import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler \
                            , CallbackQueryHandler, MessageHandler, filters
from scheduler.bot.handlers.commands import start, book, startapp
from scheduler.bot.handlers.callbacks import (
        handle_date_selection, handle_appointment_selection, handle_name_input, handle_slot_selection
    )

from dotenv import load_dotenv

# Loading Env variables
load_dotenv()

# scheduler_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

TOKEN = os.getenv("TOKEN")
# BOT_USER = os.getenv("BOT_USERNAME")
API_TOKEN = os.getenv('API_TOKEN')
SESSION_ID = os.getenv("SESSION_ID")


def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.bot_data["token"] = API_TOKEN
    application.bot_data['session_id'] = SESSION_ID
    
    # Command Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("book", book))
    application.add_handler(CommandHandler("startapp", startapp))
    
    # Callback query handler
    application.add_handler(CallbackQueryHandler(handle_slot_selection, pattern=r'^slot_\d+$'))
    application.add_handler(CallbackQueryHandler(handle_appointment_selection, pattern=r'^\d+$'))
    
    # Message handler for text messages (excluding commands)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name_input))
    
    
    application.run_polling()
        
        

if __name__ == "__main__":
    main()