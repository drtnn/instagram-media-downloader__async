from aiogram.types import Message
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default.generate import default_keyboard
from loader import dp, bot
from random import randint
from utils.db_api.database import User


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: Message):
    _, user_exists = await User.add(user_id=message.from_user.id, first_name=message.from_user.first_name,
                                    username=message.from_user.username)
    await message.answer(
        text='🙋🏻‍♂️ Привет, я бот для скачивания публикаций из <pre>Instagram</pre>.\n\n🔗 Просто отправь ссылку на пост, историю, хайлайт или никнейм.\n\n💬 Информация по всем функциям бота доступна по команде /help\n\n🗣 Подписывайся на <a href="https://t.me/InstaMediaDownload"><b>ТГК Скачать с Instagram</b></a> и узнавай обо всех обновлениях первым!',
        reply_markup=default_keyboard)
