from aiogram.types import Message
from loader import dp
from utils.db_api.database import User


@dp.message_handler(is_admin=True, commands=['count_users'])
async def bot_count_users(message: Message):
    count_users = await User.count_users()
    await message.answer(f'🤖 В базе данных {count_users} пользователя(ей)')
