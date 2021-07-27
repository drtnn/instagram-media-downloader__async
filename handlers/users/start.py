from aiogram.types import Message
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.inline.generate import channel_keyboard
from loader import dp, bot
from utils.db_api.database import User, Subscriber
from utils.misc import get_invoice_data


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
        await Subscriber.add(user_id=referral, duration=3)
        await bot.send_message(chat_id=referral,
                               text=f'🤖 +3 дня подписки за присоединение пользователя {message.from_user.first_name}')
    await message.answer(
        '🙋🏻‍♂️ Привет, я бот для скачивания публикаций из <pre>Instagram</pre>.\n\n🔗 Просто отправь ссылку на пост, историю, хайлайт или никнейм.\n\n💬 Информация по всем функциям бота доступна по команде /help' + (f'\n\n🤖 Подписка активна до <pre>{subscriber.ended_at.strftime("%d.%m.%Y")}</pre>.' if subscriber.is_actual() else ''),
        reply_markup=channel_keyboard(link='https://t.me/InstaMediaDownload'))
    if arguments == 'subscribefor14' or arguments == 'subscribefor30' or arguments == 'subscribefor90':
        invoice_data = get_invoice_data(duration=int(arguments.replace('subscribefor', '')))
        await bot.send_invoice(chat_id=message.from_user.id, title=invoice_data['title'],
                               description=invoice_data['description'],
                               provider_token=invoice_data['provider_token'], currency=invoice_data['currency'],
                               photo_url=invoice_data['photo_url'],
                               photo_size=invoice_data['photo_size'], photo_width=invoice_data['photo_width'],
                               photo_height=invoice_data['photo_height'], is_flexible=invoice_data['is_flexible'],
                               prices=invoice_data['prices'],
                               start_parameter=invoice_data['start_parameter'],
                               payload=invoice_data['payload'])
