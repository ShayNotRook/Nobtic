from telegram import Update
from telegram.ext import ContextTypes


async def salon_selection(update: Update, context: ContextTypes) -> None:
    query = update.callback_query
    await query.answer()
    salon = query.data