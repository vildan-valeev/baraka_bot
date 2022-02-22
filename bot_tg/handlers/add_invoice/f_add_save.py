from aiogram import types
from aiogram.dispatcher import FSMContext

from data.texts import message_text
from keyboards.menu import get_inline_menu, btn_back, btn_cancel, btn_save, btn_skip
from loader import dp
from state.state import AddInvoice


@dp.message_handler(regexp=r"^(\d+)$", state=AddInvoice.S5)
async def add_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text[:7])
    text = message_text.get('add_save', 'Ошибка')
    data = await state.get_data()
    template_data = f"<i>" \
                    f"{message_text.get('supplier', 'Ошибка')}: {data.get('supplier')}\n" \
                    f"{message_text.get('vendor_code', 'Ошибка')}: {data.get('vendor_code')}\n" \
                    f"{message_text.get('amount', 'Ошибка')}: {data.get('amount')}\n" \
                    f"{message_text.get('price', 'Ошибка')}: {data.get('price')}\n" \
                    f"</i>"
    menu = await get_inline_menu()
    menu.add(btn_save).add(btn_back, btn_cancel)
    await message.answer(text=text+template_data, parse_mode=types.ParseMode.HTML, reply_markup=menu)
    await AddInvoice.S6.set()


@dp.callback_query_handler(text='btn_skip', state=AddInvoice.S5)
async def skip_add_price(query: types.CallbackQuery, ):
    await query.answer()
    text = message_text.get('add_save', 'Ошибка')
    menu = await get_inline_menu()
    menu.insert(btn_back).insert(btn_cancel)
    await query.answer()
    await query.message.edit_text(text, reply_markup=menu, parse_mode=types.ParseMode.HTML)
    await AddInvoice.S6.set()


# если введены не цифры, то попадает в этот хендлер
@dp.message_handler(state=AddInvoice.S5)
async def add_cost_error(message: types.Message, state: FSMContext):
    text = message_text.get('add_price', 'Ошибка')
    wrong_text = message_text.get('wrong_text', 'Ошибка')
    menu = await get_inline_menu()
    menu.add(btn_back, btn_cancel)
    data = await state.get_data()
    if 'price' in data:
        menu.insert(btn_skip)
    await message.answer(wrong_text+text, parse_mode=types.ParseMode.HTML, reply_markup=menu)
    await AddInvoice.S5.set()
