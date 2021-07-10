from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp, database


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message):
    try:
        await database.add_new_user(user_id=message.from_user.id, username=message.from_user.username,
                                    first_name=message.from_user.first_name, referral=message.get_args())
    except:  # Поправить исключения с БД
        from loader import bot
        from data.config import ADMINS
        await bot.send_message(ADMINS[0],
                               f'user_id={message.from_user.id}, username={message.from_user.username}, first_name={message.from_user.first_name}, referral={message.get_args()}')
    await message.answer(
        '🙋🏻‍♂️ Привет, я бот для скачивания публикаций из <pre>Instagram</pre>.\n\n🔗 Просто отправь ссылку на пост, историю, хайлайт или никнейм.\n\n💬 Информация по всем функциям бота доступна по команде /help')
