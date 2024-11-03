from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# from .models import Salon

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Welcome to Nobat bot! Type /book to start booking.")
 

async def book(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    salons = ["Salon A", "Salon B", "Salon C"]  # Salon.objects.all()
    keyboard = [[InlineKeyboardButton(salon, callback_data=salon)] for salon in salons]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text("Choose a salon:", reply_markup=reply_markup)
    
    
async def salon_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    salon = query.data # Salon selected by user
    
    times = ["10:00AM", "11:00AM", "12:00PM"]
    keyboard = [[InlineKeyboardButton(time, callback_data=f"{salon}, {time}")] for time in times]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=f"Available times for {salon}", reply_markup=reply_markup)


async def confirm_appointment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    salon, time = query.data.split(',')
    await query.edit_message_text(text=f"Appointment confirmed at {salon} for {time}.")

def main():
    application = ApplicationBuilder().token("7887786324:AAHeLL7-W7goUT45ftDgqwL4dt5773h1euc").build()
    
    # Commands and Callback query handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("book", book))
    application.add_handler(CallbackQueryHandler(salon_selection))
    application.add_handler(CallbackQueryHandler(confirm_appointment))
    
    # Start polling for updates
    application.run_polling()
    
    
    
if __name__ == "__main__" :
    main()