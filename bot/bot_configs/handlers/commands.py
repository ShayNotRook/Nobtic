from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from ..utils.api import get_apps_by_salon_id



async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hi!')
    
    
async def book(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Booked!')
    
    
async def startapp(update: Update, context: CallbackContext) -> None:
    try:
        salon_id = int(context.args[0])
        token = context.bot_data.get("token")
        session_id = context.bot_data.get("session_id")
        if not token:
            await update.message.reply_text("Authorization token is missing")
            return
        
        appointments = await get_apps_by_salon_id(salon_id, session_id)
        if appointments:
            keyboard = [
                [InlineKeyboardButton(f"Appointment ID: {app['id']}, Day: {app['day_of_week']}", callback_data=str(app['id']))]
                for app in appointments
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text("یک نوبت انتخاب کنید", reply_markup=reply_markup)
        else:
            response = "No appointments found for this salon"
    except (IndexError, ValueError):
        response = "Please provide a valid salon ID"
        
    await update.message.reply_text(response)