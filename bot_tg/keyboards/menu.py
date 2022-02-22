from datetime import datetime, timedelta
from typing import List

from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


async def get_bot_commands(data: dict) -> List[types.BotCommand]:
    return [types.BotCommand(k, v) for k, v in data.items()]


async def get_inline_menu(data: dict = None) -> InlineKeyboardMarkup:
    menu = InlineKeyboardMarkup()
    if data:
        for k, v in data.items():
            menu.add(InlineKeyboardButton(text=v, callback_data=k))
    return menu


btn_back = InlineKeyboardButton(text="⬅️ Назад", callback_data="btn_back")
btn_save = InlineKeyboardButton(text="Сохранить", callback_data="btn_save")
btn_cancel = InlineKeyboardButton(text="❌ Отмена", callback_data="btn_cancel")
btn_skip = InlineKeyboardButton(text="Пропустить ➡️", callback_data="btn_skip")
calendar_callback = CallbackData('calendar', 'act', 'day', 'month', 'year', 'hour', 'minute', 'edit')


def create_calendar(day=datetime.now().day, month=datetime.now().month, year=datetime.now().year, edit=0):
    inline_kb = InlineKeyboardMarkup(row_width=5)
    ignore_callback = calendar_callback.new("IGNORE", day, month, year, 0, 0, edit)  # for buttons with no answer
    # First row - Month and Year
    inline_kb.row()
    inline_kb.insert(
        InlineKeyboardButton("<< ДД", callback_data=calendar_callback.new("PREV-DAY", day, month, year, 0, 0, edit)))
    inline_kb.insert(
        InlineKeyboardButton("< ММ", callback_data=calendar_callback.new("PREV-MONTH", day, month, year, 0, 0, edit)))
    inline_kb.insert(
        InlineKeyboardButton("ММ >", callback_data=calendar_callback.new("NEXT-MONTH", day, month, year, 0, 0, edit)))
    inline_kb.insert(
        InlineKeyboardButton("ДД >>", callback_data=calendar_callback.new("NEXT-DAY", day, month, year, 0, 0, edit)))
    inline_kb.row()
    inline_kb.insert(InlineKeyboardButton(f'{day:02d}.{month:02d}.{str(year)[2:]}', callback_data=ignore_callback))
    inline_kb.row()
    timer = 1
    while timer < 24:
        inline_kb.insert(InlineKeyboardButton(
            text=f"{timer:02d}:{00:02d}",
            callback_data=calendar_callback.new("TIME", day, month, year, timer, 00, edit)))
        timer += 1
    inline_kb.insert(InlineKeyboardButton(
        text=f"00:00",
        callback_data=calendar_callback.new("TIME", day, month, year, 0, 00, edit)))
    inline_kb.add(btn_back, btn_cancel)
    if int(edit) == 1:
        inline_kb.insert(btn_skip)
    return inline_kb


async def process_calendar_selection(query, data):
    return_data = (False, None)
    temp_date = datetime(int(data['year']), int(data['month']), int(data['day']))
    if data['act'] == "IGNORE":
        await query.answer(cache_time=60)
    elif data['act'] == "TIME":
        await query.message.delete_reply_markup()  # removing inline keyboard
        return_data = True, datetime(int(data['year']), int(data['month']), int(data['day']), int(data['hour']),
                                     int(data['minute']))
    elif data['act'] == "PREV-DAY":
        prev_date = temp_date - timedelta(days=1)
        await query.message.edit_reply_markup(
            create_calendar(int(prev_date.day), int(prev_date.month), int(prev_date.year), int(data['edit'])))
    # user navigates to next year, editing message with new calendar
    elif data['act'] == "NEXT-DAY":
        next_date = temp_date + timedelta(days=1)
        edit = bool(data['edit'])
        await query.message.edit_reply_markup(
            create_calendar(int(next_date.day), int(next_date.month), int(next_date.year), int(data['edit'])))
    # user navigates to previous month, editing message with new calendar
    elif data['act'] == "PREV-MONTH":
        prev_date = temp_date - timedelta(days=30)
        await query.message.edit_reply_markup(
            create_calendar(int(prev_date.day), int(prev_date.month), int(prev_date.year), int(data['edit'])))
    elif data['act'] == "NEXT-MONTH":
        next_date = temp_date + timedelta(days=30)
        await query.message.edit_reply_markup(
            create_calendar(int(next_date.day), int(next_date.month), int(next_date.year), int(data['edit'])))
    else:
        await query.message.answer("Something went wrong!")
    return return_data
