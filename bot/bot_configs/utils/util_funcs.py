from datetime import datetime, timedelta
from enum import Enum
from typing import List

from persiantools.jdatetime import JalaliDate

from telegram import InlineKeyboardButton, InlineKeyboardMarkup 

from bot.dataclasses import Slot

class FarsiDayConvert(Enum):
    Shanbeh = 'شنبه'
    Yekshanbe = 'بکشنبه'
    Doshanbeh = 'ٔدوشنبه'
    Seshanbeh = 'سه شنبه'
    Chaharshanbeh =  'چهار شنبه'
    Panjshanbeh = 'پنج شنبه'
    Jomeh = 'جمعه'
    
    @classmethod
    def get_day_name(cls, jalali_date: JalaliDate) -> str:
        day_index = jalali_date.weekday()
        return list(cls)[day_index].value

def convert_to_jalali(g_date):
    """
    Takes a default date time object and converts it into
    a JalaliDate object
    """
    jalali_date = JalaliDate.to_jalali(g_date)
    jalali_date.strftime("%Y/%m/%d")
    
    
def build_date_keyboard(available_slots):
    keyboard = []
    row = []
    
    for index, slot in enumerate(available_slots):
        slot_date = slot.date
        jalali = str(slot.date) if slot.date else "Invalid Date"
        row.append(InlineKeyboardButton(f"{jalali} - {FarsiDayConvert.get_day_name(slot_date)}", callback_data=f"date_{index}"))
        
        # Add row to keyboard after every 3 buttons
        if (index + 1) % 3 == 0 or index == len(available_slots) - 1:
            keyboard.append(row)
            row = []
    
    return InlineKeyboardMarkup(keyboard)


def build_time_interval_keyboard(time_intervals: List[str]) -> InlineKeyboardMarkup:
    
    keyboard = []
    for index, interval in enumerate(time_intervals):
        # Create a button for each time interval
        keyboard.append(InlineKeyboardButton(interval, callback_data=f"interval_{index}"))

    # Group buttons into rows of 4
    button_layout = [keyboard[i:i + 4] for i in range(0, len(keyboard), 4)]

    return InlineKeyboardMarkup(button_layout)


def create_slot_by_date(slot: dict):
    from datetime import datetime
    from persiantools.jdatetime import JalaliDate
    
    try:
        slot_date = datetime.strptime(slot['date'], "%Y-%m-%d").date()
        j_date = JalaliDate.to_jalali(slot_date)
        return Slot(id=slot['id'], date=j_date, time_ranges=slot['time_ranges'])
    
    except (ValueError, KeyError) as e:
        print(f"Error creating slot: {e}, slot data: {slot}")
        return None


def split_time_ranges(date, time_range_str, interval_minutes=60):
    
    # Single start time case
    if '-' not in time_range_str:
        return [time_range_str]
    
    # Normal case where it contains a range of start to max start time
    start_str, end_str = time_range_str.split(' - ')
    
    start_time = datetime.combine(date.to_gregorian(), datetime.strptime(start_str, "%H:%M").time())
    end_time = datetime.combine(date.to_gregorian(), datetime.strptime(end_str, "%H:%M").time())
    
    intervals = []
    current = start_time
    while current + timedelta(minutes=interval_minutes) <= end_time:
        slot_start = current.strftime("%H:%M")
        slot_end = (current + timedelta(minutes=interval_minutes)).strftime("%H:%M")
        intervals.append(f"{slot_start}")
        current += timedelta(minutes=interval_minutes)
        
    return intervals