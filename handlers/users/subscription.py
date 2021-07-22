from aiogram.types import Message, CallbackQuery, PreCheckoutQuery
from data.config import ADMINS
from datetime import timedelta
from loader import dp, bot
from keyboards.inline.callback_datas import subscribe_callback, mutable_subscribe_callback
from keyboards.inline.generate import subscribe_keyboard
from utils.invoice_config import get_invoice_data
from utils.instagram import InstagramUser
from utils.db_api.database import Subscription, Subscriber, Purchase


@dp.message_handler(commands=['subscribe'], state='*')
async def subscribe_message_handler(message: Message):
    subscriber = await Subscriber.add(user_id=message.chat.id, subs=0)
    await message.answer(
        text=f'🕵🏻‍♂️ Здесь ты можешь докупить месячные подписки на 3, 5 и 10 аккаунтов\n\n<i>Доступно подписок – {subscriber.subs_limit}</i>',
        reply_markup=subscribe_keyboard())


@dp.callback_query_handler(mutable_subscribe_callback.filter(), state='*')
async def mutable_subscribe_callback_query_handler(call: CallbackQuery, callback_data: dict):
    invoice_data = get_invoice_data(username='', accounts_count=int(callback_data['count']))
    await bot.send_invoice(chat_id=call.from_user.id, title=invoice_data['title'],
                           description=invoice_data['description'],
                           provider_token=invoice_data['provider_token'], currency=invoice_data['currency'],
                           photo_url=invoice_data['photo_url'],
                           photo_size=invoice_data['photo_size'], photo_width=invoice_data['photo_width'],
                           photo_height=invoice_data['photo_height'], is_flexible=invoice_data['is_flexible'],
                           prices=invoice_data['prices'],
                           start_parameter=invoice_data['start_parameter'],
                           payload=invoice_data['payload'])


@dp.callback_query_handler(subscribe_callback.filter(), state='*')
async def subscribe_callback_query_handler(call: CallbackQuery, callback_data: dict):
    user = await InstagramUser(callback_data['username']).start()
    if await Subscription.exists(call.from_user.id, callback_data['username']):
        await call.answer(text=f'🕵🏻‍♂️ Подписка на @{callback_data["username"]} уже оформлена')
    elif user:
        subscriber = await Subscriber.add(user_id=call.from_user.id, subs=0)
        if call.from_user.id in ADMINS or subscriber.subs_limit > 0:
            subscription = await subscriber.subscribe(callback_data["username"])
            await bot.send_message(chat_id=call.from_user.id,
                                   text=f'🕵🏻‍♂️ Подписка на @{callback_data["username"]} успешно оформлена и будет активна по {(subscription.created_date + timedelta(30)).strftime("%d.%m.%Y")}')
        else:
            invoice_data = get_invoice_data(username=callback_data['username'], accounts_count=3)
            await bot.send_invoice(chat_id=call.from_user.id, title=invoice_data['title'],
                                   description=invoice_data['description'],
                                   provider_token=invoice_data['provider_token'], currency=invoice_data['currency'],
                                   photo_url=invoice_data['photo_url'],
                                   photo_size=invoice_data['photo_size'], photo_width=invoice_data['photo_width'],
                                   photo_height=invoice_data['photo_height'], is_flexible=invoice_data['is_flexible'],
                                   prices=invoice_data['prices'],
                                   start_parameter=invoice_data['start_parameter'],
                                   payload=invoice_data['payload'])
    else:
        await call.answer(f'🕵🏻‍♂️ Невозможно оформить подписку на пользователя @{callback_data["username"]}')


@dp.pre_checkout_query_handler(lambda query: True, state='*')
async def pre_subscribe_callback_query_handler(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=['successful_payment'], state='*')
async def subscribe_successful_payment(message: Message):
    await Purchase(user_id=message.chat.id, amount=message.successful_payment.total_amount).create()
    payload = message.successful_payment.invoice_payload.split(':')
    subscriber = await Subscriber.add(user_id=message.chat.id, subs=int(payload[1]))
    if payload[2] != '':
        subscription = await subscriber.subscribe(payload[2])
        await message.answer(
            text=f'🕵🏻‍♂️ Подписка на @{payload[2]} успешно оформлена и будет активна до {(subscription.created_date + timedelta(30)).strftime("%d.%m.%Y")}\n\n<i>Доступно подписок – {subscriber.subs_limit}</i>')
    else:
        await message.answer(text=f'🕵🏻‍♂️ Подписки успешно приобретены\n\n<i>Доступно подписок – {subscriber.subs_limit}</i>')
