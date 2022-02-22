from aiogram import types
from aiogram.dispatcher import FSMContext

from data.texts import message_text
from keyboards.menu import get_inline_menu, btn_back, btn_skip, btn_cancel
from loader import dp
from state.state import AddInvoice


@dp.message_handler(regexp=r"^(\d+)$", state=AddInvoice.S2)
async def add_date(message: types.Message, state: FSMContext):
    text = message_text.get('add_vendor_code', 'Ошибка')
    menu = await get_inline_menu()
    menu.insert(btn_back).insert(btn_cancel)
    await state.update_data(supplier=message.text)
    await message.answer(text, reply_markup=menu, parse_mode=types.ParseMode.HTML)
    await AddInvoice.S3.set()


@dp.callback_query_handler(text='btn_skip', state=AddInvoice.S2)
@dp.callback_query_handler(text='btn_back', state=AddInvoice.S4)
async def back_add_date(query: types.CallbackQuery, state: FSMContext):
    await query.answer()
    text = message_text.get('add_vendor_code', 'Ошибка')
    data = await state.get_data()
    current_input = data.get('vendor_code', '')
    menu = await get_inline_menu()
    menu.add(btn_back, btn_cancel)
    data = await state.get_data()
    if 'vendor_code' in data:
        menu.insert(btn_skip)
    await query.message.edit_text(f'{text}\n<i>{current_input}</i>', reply_markup=menu, parse_mode=types.ParseMode.HTML)
    await AddInvoice.S3.set()


# если введены не цифры, то попадает в этот хендлер
@dp.message_handler(state=AddInvoice.S2)
async def add_cost_error(message: types.Message, state: FSMContext):
    text = message_text.get('add_supplier', 'Ошибка')
    wrong_text = message_text.get('wrong_text', 'Ошибка')
    menu = await get_inline_menu()
    menu.add(btn_back, btn_cancel)
    data = await state.get_data()
    if 'supplier' in data:
        menu.insert(btn_skip)
    await message.answer(wrong_text + text, parse_mode=types.ParseMode.HTML, reply_markup=menu)
    await AddInvoice.S2.set()

