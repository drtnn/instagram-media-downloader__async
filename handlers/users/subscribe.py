from aiogram.types import Message, CallbackQuery, PreCheckoutQuery
from loader import dp, bot
from keyboards.inline.callback_datas import subscribe_callback
from keyboards.inline.generate import subscribe_keyboard
from utils.db_api.database import Subscriber, Purchase
from utils.misc import get_invoice_data


@dp.message_handler(commands=['subscribe'], state='*')
async def subscribe_message_handler(message: Message):
    subscriber = await Subscriber.add(user_id=message.chat.id, duration=0)
    if subscriber.is_actual():
        await message.answer(
            text=f'🤖 Твоя подписка действует до <pre>{subscriber.ended_at.strftime("%d.%m.%Y")}</pre>\nХочешь продлить подписку? Кликай на кнопку ниже!',
            reply_markup=subscribe_keyboard())
    else:
        await message.answer(
            text='🤖 Подписка дает возможность удобно скачивать любой контент из <pre>Instagram</pre>\nХочешь пользоваться ботом бесплатно? /referral\nХочешь подключить подписку? Кликай на кнопку ниже!',
            reply_markup=subscribe_keyboard())


@dp.callback_query_handler(subscribe_callback.filter(), state='*')
async def subscribe_callback_query_handler(call: CallbackQuery, callback_data: dict):
    invoice_data = get_invoice_data(duration=int(callback_data['duration']))
    await bot.send_invoice(chat_id=call.from_user.id, title=invoice_data['title'],
                           description=invoice_data['description'],
                           provider_token=invoice_data['provider_token'], currency=invoice_data['currency'],
                           photo_url=invoice_data['photo_url'],
                           photo_size=invoice_data['photo_size'], photo_width=invoice_data['photo_width'],
                           photo_height=invoice_data['photo_height'], is_flexible=invoice_data['is_flexible'],
                           prices=invoice_data['prices'],
                           start_parameter=invoice_data['start_parameter'],
                           payload=invoice_data['payload'])


@dp.pre_checkout_query_handler(lambda query: True, state='*')
async def pre_subscribe_callback_query_handler(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=['successful_payment'], state='*')
async def subscribe_successful_payment(message: Message):
    await Purchase(user_id=message.chat.id, amount=message.successful_payment.total_amount).create()
    payload = message.successful_payment.invoice_payload.split(':')
    subscriber = await Subscriber.add(user_id=message.chat.id, duration=int(payload[1]))
    await message.answer(text=f'🤖 Подписка успешно офрмлена и будет активна до <pre>{subscriber.ended_at.strftime("%d.%m.%Y")}</pre>')
