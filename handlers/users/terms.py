from aiogram.types import Message
from aiogram.utils.markdown import text
from data.config import BOT_NAME
from loader import dp


@dp.message_handler(commands=['terms'], state='*')
async def referral_message_handler(message: Message):
    await message.answer(
        text=text(
            f'Правила пользования ботом {BOT_NAME}:',
            '• '
        )
    )
