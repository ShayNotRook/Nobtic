from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from scheduler.bot.utils.api import book_appointment, get_apppointments_by_slot_id

def handle_date_selection(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"Selected date: {query.data}")
    
    
    
async def handle_slot_selection(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    
    slot_id = query.data.split("_")[1]
    token = context.bot_data.get("token")
    
    appointments = await get_apppointments_by_slot_id(slot_id=slot_id, token=token)
    if appointments:
        keyboard = [
            [InlineKeyboardButton(f"Appointment ID: {app['id']} Date: {app['date']} \
                Time: {app['app_start']} - {app['app_end']}", callback_data=app['id'])]
            for app in appointments
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Choose an appointment", reply_markup=reply_markup)
    else:
        await query.edit_message_text("No appointment found for this slot")

async def handle_appointment_selection(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    
    appointment_id = query.data
    context.user_data['appointment_id'] = appointment_id
    
    await query.edit_message_text(text=f"Selected appointment ID: {appointment_id} \
                                  Please enter your name to proceed appointment")
    
    
    
async def handle_name_input(update: Update, context: CallbackContext) -> None:
    name = update.message.text
    appointment_id = context.user_data.get('appointment_id')
    token = context.bot_data.get("token")
    
    if not appointment_id:
        await update.message.reply_text("No appointment selected.")
        return
    
    if not token:
        await update.message.reply_text("Authorization token is missing")
        return
    
    response = await book_appointment(appointment_id=appointment_id, name=name, token=token)
    if response.get('success'):
        await update.message.reply_text(f"Appointment booked successfully for {name}")
    else:
        await update.message.reply_text("Failed to book appointment. Please try again.")