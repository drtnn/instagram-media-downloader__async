from aiogram.types import Message
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp
from utils.db_api.database import User


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: Message):
    await User.add_user(user_id=message.from_user.id, first_name=message.from_user.first_name,
                        username=message.from_user.username,
                        referral=int(message.get_args()) if message.get_args() else None)
    await message.answer(
        '🙋🏻‍♂️ Привет, я бот для скачивания публикаций из <pre>Instagram</pre>.\n\n🔗 Просто отправь ссылку на пост, историю, хайлайт или никнейм.\n\n💬 Информация по всем функциям бота доступна по команде /help')
