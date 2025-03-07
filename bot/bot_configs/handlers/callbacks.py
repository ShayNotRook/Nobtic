import logging

from aiohttp import FormData

from telegram import (Update, InlineKeyboardButton, InlineKeyboardMarkup,
                      KeyboardButton, ReplyKeyboardMarkup)

from telegram.ext import (ContextTypes, ConversationHandler, CallbackQueryHandler,
                                MessageHandler, filters, CommandHandler)

from bot.bot_configs.utils.util_funcs import (build_date_keyboard, split_time_ranges,
                                              build_time_interval_keyboard)

from bot.bot_configs.utils.api import (fetch_available_slots, send_verify_code,
                                       verify_code, create_appointment,
                                       update_appointment)


async def handle_employee_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # Callback data in the form of "emp_{id}"
    emp_id = int(query.data.split("_")[1])
    salon = context.user_data.get('salon')
    
    if salon is None:
        await query.edit_message_text("خطا: اطلاعات سالن یافت نشد")
        return

    employee = next((emp for emp in salon.employees if emp.id == emp_id), None)
    if employee is None:
        await query.edit_message_text("سرویس دهنده انتخاب شده معتبر نیست")
        return
    

    # Saving selected employee for later
    context.user_data['employee'] = employee
    
    keyboard = [
        [InlineKeyboardButton(service.name, callback_data=f"svc_{service.id}")
        for service in employee.services]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=f"شما {employee.name} را انتخاب کردید. لطفاً یک سرویس را انتخاب کنید:",
        reply_markup=reply_markup
    )
    

async def handle_service_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    svc_id = int(query.data.split("_")[1])
    employee = context.user_data['employee']    
    service = next((svc for svc in employee.services if svc.id == svc_id), None)
    
    if service is None:
        await query.edit_message_text("سرویس انتخاب شده یافت نشد")
        return
    
    slots = await fetch_available_slots(employee_id=employee.id, service_id=service.id)
    
    context.user_data['service'] = service
    context.user_data['slots'] = slots
    print(service.id)
    markup = build_date_keyboard(slots)
    
    await query.edit_message_text("یک تاریخ را انتخاب کنید:", reply_markup=markup)

    
   
async def handle_date_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    try:
        date_id = int(query.data.split("_")[1])
    except (IndexError, ValueError):
        await query.edit_message_text("خطا در انتخاب تاریخ")
        return
    
    slots = context.user_data.get("slots", [])
    if date_id < 0 or date_id >= len(slots):
        await query.edit_message_text("تاریخ انتخاب شده معتبر نیست")
        return
    
    selected_slot = slots[date_id]
    print(selected_slot.id)
    context.user_data["selected_slot"] = selected_slot
    
    all_intervals = []
    for time_range in selected_slot.time_ranges:
        intervals = split_time_ranges(selected_slot.date, time_range)
        all_intervals.extend(intervals)
        
        
    context.user_data['intervals'] = all_intervals
    
    markup = build_time_interval_keyboard(all_intervals)
    
    formatted_date = f"{selected_slot.date.day}\\-{selected_slot.date.month}\\-{selected_slot.date.year}"
    await query.edit_message_text(
        text=f"زمان‌های موجود برای **{formatted_date}**:",
        reply_markup=markup,
        parse_mode='MarkdownV2'
    )
    
    
async def handle_interval_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    intervals = context.user_data['intervals']
    print(intervals)
    
    try:
        interval_id = int(query.data.split("_")[1])
        print(interval_id)
        selected_interval = intervals[interval_id]
    except (IndexError, ValueError):
        await query.edit_message_text("بازه انتخاب شده معتبر نیست")
        return
    
    selected_slot = context.user_data.get("selected_slot")
    
    if selected_interval is None:
        query.edit_message_text("خطا در دریافت تاریخ")
    
    context.user_data['selected_interval'] = selected_interval
    
    
    keyboard = [
        [InlineKeyboardButton(text='تایید', callback_data="proceed")],
        [InlineKeyboardButton(text='اصلاح', callback_data="edit")]
    ]
    
    
    markup = InlineKeyboardMarkup(keyboard)
    
    employee = context.user_data['employee']
    service = context.user_data['service']
    
    formatted_date = f"{selected_slot.date.day}\\-{selected_slot.date.month}\\-{selected_slot.date.year}"
    
    await query.edit_message_text(
    text=f"🎉 *نوبت شما با:* {employee.name}\n"
         f"💇‍♀️ *سرویس:* {service.name}\n"
         f"📅 *تاریخ:* {formatted_date}\n"
         f"🕑 *ساعت:* {selected_interval}\n\n"
         "✅ اگر از نوبت درخواستی مطمئن هستید گزینه *تایید* را انتخاب کنید\n"
         "✏️ برای *تصحیح* اطلاعات گزینه اصلاح را انتخاب کنید",
    reply_markup=markup,
    parse_mode="MarkdownV2"
    )



# ---- States created using ConversationHandler ----
IRAN_PHONE_REGEX = r"^(?:\+98|0)?9\d{9}$"
GET_NAME, GET_PHONE, VERIFY_PHONE, FINAL_CONFIRM, WAIT_FOR_RECEIPT = range(5)


async def proceed_final(update: Update, context: ContextTypes):
    query = update.callback_query
    await query.answer()
    print("proceed test")
    
    await query.edit_message_text("✍️ لطفاً نام خود را وارد کنید:")
    
    return GET_NAME
    

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["user_name"] = update.message.text
    
    keyboard = [
        [KeyboardButton("📱 ارسال شماره", request_contact=True)]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    await update.message.reply_text("📞 لطفاً شماره موبایل خود را وارد کنید یا دکمه زیر را بزنید:", reply_markup=reply_markup)
    print('send phone')
    return GET_PHONE


async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    import re
    
    print("test phone")
    if update.message.contact:
        phone_num = update.message.contact.phone_number
    else:
        phone_num = update.message.text.strip()
        
    if not re.match(IRAN_PHONE_REGEX, phone_num):
        await update.message.reply_text("❌ شماره وارد شده نامعتبر است. لطفاً شماره معتبر وارد کنید")
        return GET_PHONE
    
    context.user_data['phone_num'] = phone_num
    
    result = await send_verify_code(phone_num)

    if result.get('valid') == True:
        await update.message.reply_text("🔢 لطفاً کد تأیید ارسال‌شده را وارد کنید:")
        return VERIFY_PHONE
    else:
        await update.message.reply_text("❌ ارسال کد تأیید ناموفق بود. لطفاً دوباره امتحان کنید.")
        return GET_PHONE


async def verify_sent_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"DEBUG: Received update: {update.message}")  # Debugging line

    if isinstance(update, str):
        print("ERROR: update is a string, something is wrong!")
        return VERIFY_PHONE  # Prevents crashing
    
    if update.message:
        verification_code = update.message.text.strip()
    elif update.callback_query:
        query = update.callback_query
        verification_code = query.data.strip()
        await query.answer()
    else:
        await update.message.reply_text("❌ ورودی نامعتبر است. لطفاً دوباره امتحان کنید.")
        return VERIFY_PHONE
    
    phone_num = context.user_data['phone_num']

    result = await verify_code(phone_num, verification_code)
    print(f"Verifictation result: {result}")
    
    if result.get("valid"):
        await update.message.reply_text("✅ کد تأیید با موفقیت تایید شد")
        keyboard = [
            [InlineKeyboardButton(text="💾 ذخیره اطلاعات", callback_data="info_save")],
            [InlineKeyboardButton(text="🚫 عدم ذخیره", callback_data="info_clear")]
        ]
        markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("آیا می‌خواهید اطلاعات خود را ذخیره کنید؟", reply_markup=markup)
        
        return FINAL_CONFIRM
        
    else:
        return VERIFY_PHONE
    
# ---- Save/Not Save handlers ----
async def save_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    print("Data saved.")
    
    return await send_payment_info(update, context)
    
async def dont_save(update: Update, context: ContextTypes):
    query = update.callback_query
    await query.answer()
    
    print("Data not saved.")
    
    return await send_payment_info(update, context)

def comma_adder(digits_str):
    """
        Adds Comma after every three digits in a string of digits.
        
        Args:
            digits_str: A string containing only digits
        
        Returns:
            A string with commas inserted after every three digits.
    """
    result = []
    for i, digit in enumerate(reversed(digits_str)):
        if i > 0 and i % 3 == 0:
            result.append(",")
        result.append(digit)
    return "".join(reversed(result))

# ---- Payment Step Handlers ----
async def send_payment_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    employee = context.user_data.get('employee')
    card_info = employee.card_num
    
    service_price = context.user_data['service'].price
    converted_price = comma_adder(str(service_price))
    
    message = (
        f"لطفا مبلغ *{converted_price}* تومان* به حساب زیر واریز کنید*\n\n"
        f"*{card_info}*\n\n"
        "لطفا پس از واریز, فیش واریز خود را به صورت متن یا عکس ارسال کنید\\."
    )
    
    if update.callback_query:
        await update.callback_query.edit_message_text(message, parse_mode="MarkdownV2")
    else:
        await update.message.reply_text(message, parse_mode="MarkdownV2")
    
    payload = {
        "customer_name": context.user_data['user_name'],
        "service": context.user_data['service'].id,
        "app_start": context.user_data['selected_interval'],
        "slot": context.user_data['selected_slot'].id,
        "chat_id": context._chat_id
    }
    
    print(f"Payload: {payload}")
    result = await create_appointment(payload)
    context.user_data['app_id'] = result['id']
    
    return WAIT_FOR_RECEIPT

async def handle_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Base data class
    payload = FormData()
    payload.add_field("status", "در انتظار تایید")
    
    if update.message.photo:
        import io
        
        file_id = update.message.photo[-1].file_id
        file_info = await context.bot.get_file(file_id)
        
        # Downloaded Image
        receipt_img = await file_info.download_as_bytearray()
        # receipt_txt = update.message.caption or ""
        payload.add_field("receipt_img", io.BytesIO(receipt_img), filename='test.jpeg', content_type="image/jpeg")
    
    elif (receipt_txt := update.message.text):
        payload.add_field("receipt_txt", receipt_txt)
    
    
    print(payload)
    response = await update_appointment(app_id=context.user_data['app_id'], payload=payload)
    print(response)
    await update.message.reply_text("رسید پرداخت دریافت شد. نوبت شما در انتظار تأیید می‌باشد")
    
    ConversationHandler.END



async def cancel(update: Update, context: ContextTypes):
    context.user_data.clear()
    
    await update.message.edit_text("درخواست شما لغو شد!")
    
    ConversationHandler.END


# ---- Conversation Struct ----
conv_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(proceed_final, pattern="^proceed$")],
    states = {
        GET_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
        GET_PHONE: [
            MessageHandler(filters.CONTACT, get_phone),
            MessageHandler(filters.TEXT, get_phone)
        ],
        VERIFY_PHONE: [
            MessageHandler(filters.TEXT & filters.Regex(r"^\d{6}$"), verify_sent_code)
        ],
        FINAL_CONFIRM: [
            CallbackQueryHandler(save_info, pattern="^info_save$"),
            CallbackQueryHandler(dont_save, pattern="^info_clear$")
        ],
        WAIT_FOR_RECEIPT: [
            MessageHandler(filters.PHOTO, handle_receipt),
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_receipt)
        ]
    },
    fallbacks = [CommandHandler('cancel', cancel)],
    per_user=True,
    per_message=False
)

