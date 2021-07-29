from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from states.admin import Mailing
from utils.db_api.database import User


@dp.message_handler(is_admin=True, commands=['mailing'])
async def bot_mailing(message: Message):
    await message.answer('🤖 Присылай сообщение для рассылки')
    await Mailing.text.set()


@dp.message_handler(is_admin=True, state=Mailing.text)
async def bot_mailing_text(message: Message, state: FSMContext):
    await state.update_data(tex=message.text)
    await state.reset_state()
    await User.mailing(bot=bot, text=message.text)
