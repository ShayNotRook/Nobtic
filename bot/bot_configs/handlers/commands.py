import os

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

import django

from asgiref.sync import sync_to_async

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

django.setup()


from scheduler.models import Salon

from ..utils.api import fetch_salon_data



# Aync ORM Helper Function (Converting Salon object retriever to an async function)
async def get_salon_by_slug(slug):
    return await sync_to_async(Salon.objects.get)(slug=slug)


# Base start function, If received an argument, It parses that arg into a slug
# param and retrieves the salon instance by that slug, using an API.
async def start(update: Update, context: CallbackContext) -> None:
    args = context.args
    if args:
        salon_slug = args[0]
        salon = await fetch_salon_data(slug=salon_slug)
        
        if not salon:
            update.message.reply_text("متاسفانه اطلاعات سالن در دسترس نیست.")
            return
        
        context.user_data['salon'] = salon
            
        salon_name = salon.name
        employees = salon.employees
        
        keyboard = [
            [InlineKeyboardButton(employee.name, callback_data=f"emp_{employee.id}")
            for employee in employees]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
        f"به سیستم رزرو سالن زیبایی \"{salon_name}\" خوش آمدید! 🎉\n"
        "برای مشاهده خدمات و رزرو نوبت، دستورهای زیر را دنبال کنید, \n"
        "نخست سرویس دهنده ی خود را انتخاب کنید:",
        reply_markup=reply_markup
        )
        
        
    else:
        await update.message.reply_text(
            "به ربات رزرو سالن زیبایی خوش آمدید! 💇‍♀️💅\n"
            "لطفاً از لینک مخصوص سالن خود استفاده کنید یا با پشتیبانی تماس بگیرید."
        )
    
    
async def book(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Booked!')
    
