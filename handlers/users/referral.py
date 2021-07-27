from aiogram.types import Message
from data.config import BOT_NAME
from loader import dp


@dp.message_handler(commands=['referral'], state='*')
async def referral_message_handler(message: Message):
    await message.answer(
        text=f'🤖 Пригласи друга по своей реферальной ссылке и получи 3 дня бесплатной подписки\n<code>t.me/{BOT_NAME}?start={message.chat.id}</code>')
