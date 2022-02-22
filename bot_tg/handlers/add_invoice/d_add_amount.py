from aiogram import types
from aiogram.dispatcher import FSMContext

from data.texts import message_text
from keyboards.menu import get_inline_menu, btn_cancel, btn_back, btn_skip
from loader import dp
from state.state import AddInvoice


@dp.message_handler(regexp=r"^(\d+)$", state=AddInvoice.S3)
async def date_pag(message: types.Message, state: FSMContext):

    text = message_text.get('add_amount', 'Ошибка')
    menu = await get_inline_menu()
    menu.insert(btn_back).insert(btn_cancel)
    await state.update_data(vendor_code=message.text)
    await message.answer(text, reply_markup=menu)
    await AddInvoice.S4.set()


@dp.callback_query_handler(text='btn_skip', state=AddInvoice.S3)
@dp.callback_query_handler(text='btn_back', state=AddInvoice.S5)
async def back_options(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    text = message_text.get('add_amount', 'Ошибка')
    data = await state.get_data()
    current_input = data.get('amount', '')
    menu = await get_inline_menu()
    menu.add(btn_back, btn_cancel,)

    data = await state.get_data()
    if 'amount' in data:
        menu.insert(btn_skip)
    await callback_query.message.edit_text(f'{text}\n<i>{current_input}</i>', reply_markup=menu)
    await AddInvoice.S4.set()


# если введены не цифры, то попадает в этот хендлер
@dp.message_handler(state=AddInvoice.S3)
async def add_cost_error(message: types.Message, state: FSMContext):
    text = message_text.get('add_vendor_code', 'Ошибка')
    wrong_text = message_text.get('wrong_text', 'Ошибка')
    menu = await get_inline_menu()
    menu.add(btn_back, btn_cancel)
    data = await state.get_data()
    if 'vendor_code' in data:
        menu.insert(btn_skip)
    await message.answer(wrong_text + text, parse_mode=types.ParseMode.HTML, reply_markup=menu)
    await AddInvoice.S3.set()
