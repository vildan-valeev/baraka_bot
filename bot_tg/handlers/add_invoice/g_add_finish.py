from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from data.config import ADMINS
from data.texts import message_text
from loader import dp
from state.state import AddInvoice
from utils.iiko_api import create_invoice


@dp.callback_query_handler(text='btn_save', state=AddInvoice.S6)
async def add_price(query: CallbackQuery, state: FSMContext):
    await query.answer()
    data = await state.get_data()
    print(data)
    result = await create_invoice(data)
    if result:
        text = message_text.get('complete_save', 'Ошибка')
        await query.message.edit_text(text, disable_web_page_preview=True, )
    else:
        text = message_text.get('error', 'Ошибка')
        await query.message.edit_text(text, disable_web_page_preview=True, )
        text = message_text.get('notify_admin_error')
        await query.bot.send_message(chat_id=ADMINS[0], text=text, disable_web_page_preview=True)
    await state.finish()
