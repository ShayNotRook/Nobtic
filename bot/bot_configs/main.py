import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from telegram.ext import ApplicationBuilder, CommandHandler \
                            , CallbackQueryHandler, MessageHandler, filters
                            
from bot.bot_configs.handlers.commands import start, book
from bot.bot_configs.handlers.callbacks import (
    handle_employee_selection, handle_service_selection, handle_date_selection,
    handle_interval_selection, conv_handler)


from dotenv import load_dotenv

# Loading Env variables
load_dotenv()


TOKEN = os.getenv("TOKEN")
API_TOKEN = os.getenv('API_TOKEN')
SESSION_ID = os.getenv("SESSION_ID")


def main() -> None:
    application = ApplicationBuilder() \
                    .token(TOKEN) \
                    .build()
    

    # Command Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("book", book))
    
    
    # Callback query handler
    application.add_handler(CallbackQueryHandler(handle_employee_selection, pattern=r'^emp_'))
    application.add_handler(CallbackQueryHandler(handle_service_selection, pattern=r'^svc_'))
    application.add_handler(CallbackQueryHandler(handle_date_selection, pattern=r'^date_'))
    application.add_handler(CallbackQueryHandler(handle_interval_selection, pattern=r'^interval_'))
    
    # Conversation handler
    application.add_handler(conv_handler)
    
    
    # Loop runner
    application.run_polling()
        
        

if __name__ == "__main__":
    main()