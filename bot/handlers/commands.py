from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from scheduler.models import Salon

async def start(update: Update, context:ContextTypes) -> None:
    await update.message.reply_text("Welcome! type /book to schedule an appointment.")
    
    
async def book(update: Update, context: ContextTypes) -> None:
    # Example logic for booking
    salons = Salon.objects.all().values_list('name', flat=True)
    keyboard = [[InlineKeyboardButton(salon, callback_data=salon)] for salon in salons]
    reply_text = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text("Choose a salon:", reply_markup=reply_text)