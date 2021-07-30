from aiogram.types import Message
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default.generate import default_keyboard
from keyboards.inline.generate import channel_keyboard
from loader import dp, bot
from random import randint
from utils.db_api.database import User, Subscriber


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: Message):
    arguments = message.get_args()
    referral = int(arguments) if arguments and arguments.isdigit() else None
    _, user_exists = await User.add_user(user_id=message.from_user.id, first_name=message.from_user.first_name,
                                         username=message.from_user.username,
                                         referral=referral)
    if not user_exists:
        subscriber = await Subscriber.add(user_id=message.from_user.id, duration=7)
    else:
        subscriber = await Subscriber.add(user_id=message.from_user.id, duration=0)
    if referral and not user_exists and referral != message.chat.id:
        await Subscriber.add(user_id=referral, duration=randint(3, 7))
        await bot.send_message(chat_id=referral,
                               text=f'🤖 +3 дня подписки за присоединение пользователя {message.from_user.first_name}')
    await message.answer(
        text='🙋🏻‍♂️ Привет, я бот для скачивания публикаций из <pre>Instagram</pre>.\n\n🔗 Просто отправь ссылку на пост, историю, хайлайт или никнейм.\n\n💬 Информация по всем функциям бота доступна по команде /help' + (
            f'\n\n🤖 Подписка активна до <pre>{subscriber.ended_at.strftime("%d.%m.%Y")}</pre>.' if subscriber.is_actual() else ''),
        reply_markup=default_keyboard)
    await message.answer(text='🗣 Подписывайся на <a href="https://t.me/InstaMediaDownload"><b>ТГК Скачать с Instagram</b></a> и узнавай обо всех обновлениях первым!', reply_markup=channel_keyboard(link='https://t.me/InstaMediaDownload'))
