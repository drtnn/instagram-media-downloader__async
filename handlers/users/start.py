from aiogram.types import Message
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.inline.generate import channel_keyboard
from loader import dp, bot
from utils.db_api.database import User, Subscriber


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: Message):
    referral = int(message.get_args()) if message.get_args() else None
    _, user_exists = await User.add_user(user_id=message.from_user.id, first_name=message.from_user.first_name,
                                         username=message.from_user.username,
                                         referral=referral)
    if referral and not user_exists and referral != message.chat.id:
        subscriber = await Subscriber.add(user_id=referral, subs=1)
        await bot.send_message(chat_id=referral,
                               text=f'🕵🏻‍♂️ +1 подписка за присоединение пользователя {message.from_user.first_name}\n\n<i>Доступно подписок – {subscriber.subs_limit}</i>')
    await message.answer(
        '🙋🏻‍♂️ Привет, я бот для скачивания публикаций из <pre>Instagram</pre>.\n\n🔗 Просто отправь ссылку на пост, историю, хайлайт или никнейм.\n\n💬 Информация по всем функциям бота доступна по команде /help',
        reply_markup=channel_keyboard(link='https://t.me/InstaMediaDownload'))
