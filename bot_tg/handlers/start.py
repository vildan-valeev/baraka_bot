from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.menu import get_bot_commands
from loader import dp
from data.texts import message_text, commands
from utils.is_admin import is_admin


@dp.message_handler(commands='start', state='*')
async def cmd_start(message: types.Message, state: FSMContext):
    """Стартовая"""
    await state.reset_data()  # сброс состояния
    await state.reset_state()  # сброс состояния

    if is_admin(message.from_user.id):
        text = message_text.get('hello', 'Ошибка')
        # формируем меню(команды) из списка кнопок
        commands_ = await get_bot_commands(commands)
        # вывод
        await dp.bot.set_my_commands(commands=commands_, scope=types.BotCommandScopeChat(chat_id=message.chat.id))

        await message.answer(text=text, reply_markup=types.ReplyKeyboardRemove(),
                             disable_web_page_preview=True, parse_mode=types.ParseMode.HTML, )
    else:
        text = message_text.get('not_admin', 'Ошибка')
        await message.answer(text=text, reply_markup=types.ReplyKeyboardRemove())
