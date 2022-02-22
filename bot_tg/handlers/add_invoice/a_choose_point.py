from aiogram import types
from aiogram.dispatcher import FSMContext

from data.texts import commands, message_text, points
from keyboards.menu import get_bot_commands, get_inline_menu, btn_cancel, btn_skip
from loader import dp
from state.state import AddInvoice


from utils.is_admin import is_admin


@dp.message_handler(commands='add_invoice', state='*')
async def add_point_a(message: types.Message, state: FSMContext):
    """Начало создания накладной - выбор точки"""
    await state.reset_data()
    await state.reset_state()

    commands_ = await get_bot_commands(commands)
    await dp.bot.set_my_commands(commands=commands_, scope=types.BotCommandScopeChat(chat_id=message.chat.id))
    text = message_text.get('choose_point_to_invoice', 'Ошибка')
    # проверка прав
    if is_admin(message.from_user.id):
        menu = await get_inline_menu(points)
        menu.add(btn_cancel)
        await message.answer(text=text, reply_markup=menu,
                             disable_web_page_preview=True, parse_mode=types.ParseMode.HTML, )
    else:
        text = message_text.get('not_admin', 'Ошибка')
        await message.answer(text=text, reply_markup=types.ReplyKeyboardRemove())

    await AddInvoice.S1.set()


@dp.callback_query_handler(text='btn_back', state=AddInvoice.S2)
async def back_add_point_a(query: types.CallbackQuery, state: FSMContext):
    """начало создания объявления объявления - ввод point_a"""
    text = message_text.get('choose_point_to_invoice', 'Ошибка')
    menu = await get_inline_menu(points)
    data = await state.get_data()
    current_input = data.get('point', '')
    if 'point' in data:  # добавляем кнопку скип если ранее уже вводили, т.е. возврат
        menu.insert(btn_skip)
    await query.answer()
    await query.message.edit_text(text=f'{text}\n<i>{current_input}</i>',
                                  parse_mode=types.ParseMode.HTML,
                                  reply_markup=menu.insert(btn_cancel))
    await AddInvoice.S1.set()

