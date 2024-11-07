from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes


async def salon_selection(update: Update, context: ContextTypes) -> None:
    query = update.callback_query
    await query.answer()
    salon = query.data
    
    times = ['10:00AM', '12:00AM', '4:00PM']
    keyboard = [[InlineKeyboardButton(time, callback_data=f"{time} for {salon}")] for time in times]
    reply_mark = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=f"Available times for {salon}", reply_markup=reply_mark)
    
    
    
async def confirm_appointment(update: Update, context: ContextTypes) -> None:
    query = update.callback_query
    await query.answer()
    salon, time = query.data.split(',')
    await query.edit_message_text(text=f"Appointment confirmed at {time} for {salon}")