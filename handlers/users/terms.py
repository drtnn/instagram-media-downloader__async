from aiogram.types import Message
from data.config import BOT_NAME
from loader import dp


@dp.message_handler(commands=['terms'], state='*')
async def referral_message_handler(message: Message):
    await message.answer(
        text=f'Правила пользования ботом {BOT_NAME}:')
