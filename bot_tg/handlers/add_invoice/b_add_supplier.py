from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.menu import get_inline_menu, btn_back, btn_cancel, btn_skip
from loader import dp
from state.state import AddInvoice
from data.texts import message_text


@dp.callback_query_handler(text_contains='point_', state=AddInvoice.S1)
async def add_point_b(query: types.CallbackQuery, state: FSMContext):
    await query.answer()
    text = message_text.get('add_supplier', 'Ошибка')
    menu = await get_inline_menu()
    menu.add(btn_back, btn_cancel)
    await state.update_data(point=query.data)
    await query.message.edit_text(text, reply_markup=menu, parse_mode=types.ParseMode.HTML)
    await AddInvoice.S2.set()


@dp.callback_query_handler(text='btn_skip', state=AddInvoice.S1)
@dp.callback_query_handler(text='btn_back', state=AddInvoice.S3)
async def back_add_point_b(query: types.CallbackQuery, state: FSMContext):
    await query.answer()
    text = message_text.get('add_supplier', 'Ошибка')
    data = await state.get_data()
    current_input = data.get('supplier', '')
    menu = await get_inline_menu()
    menu.add(btn_back, btn_cancel)
    data = await state.get_data()
    if 'supplier' in data:
        menu.insert(btn_skip)
    await query.answer()
    await query.message.edit_text(f'{text}\n<i>{current_input}</i>', reply_markup=menu, parse_mode=types.ParseMode.HTML)
    await AddInvoice.S2.set()
