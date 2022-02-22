from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, ParseMode

from data.texts import message_text
from loader import dp


@dp.callback_query_handler(text='btn_cancel', state='*')
async def cancel(query: CallbackQuery, state: FSMContext):
    await query.answer()
    text = message_text.get('cancel', 'Ошибка')
    await query.message.answer(text=text)
    await state.finish()


@dp.message_handler()
async def contacts(message: Message, state: FSMContext):
    await state.reset_state()
    text = message_text.get('not_understand', 'Ошибка')
    await message.answer(text=text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
