from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

from scheduler.models import Salon
    
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




