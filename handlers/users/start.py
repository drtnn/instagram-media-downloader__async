from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
# from loader import dp, database
from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    # await database.add_new_user(user_id=message.from_user.id, username=message.from_user.username, first_name=message.from_user.first_name, referral=message.get_args())
    await message.answer(
        '🙋🏻‍♂️ Привет, я бот для скачивания публикаций из <pre>Instagram</pre>.\n\n🔗 Просто отправь ссылку на пост, историю или никнейм.\n\n💬 Информация по всем функциям бота доступна по команде /help')
