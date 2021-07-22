from aiogram.types import Message
from data.config import BOT_NAME
from loader import dp


@dp.message_handler(commands=['referral'], state='*')
async def referral_message_handler(message: Message):
    await message.answer(
        text=f'🕵🏻‍♂️ Пригласи пользователя по своей реферальной ссылке и получи 1 бесплатную месячную подписку\nt.me/{BOT_NAME}?start={message.chat.id}')
