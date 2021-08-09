from aiogram.types import Message, CallbackQuery
from loader import dp, bot
from keyboards.inline.callback_datas import subscribe_callback
from keyboards.inline.generate import subscribe_keyboard, payment_keyboard
from utils.db_api.database import Subscriber
from utils.payment.invoice_data import get_invoice_data
from utils.payment.yoomoney.quickpay import payment_link


@dp.message_handler(commands=['subscribe'], state='*')
async def subscribe_message_handler(message: Message):
    subscriber = await Subscriber.add(user_id=message.chat.id, duration=0)
    if subscriber.is_actual():
        await message.answer(
            text=f'🤖 Твоя подписка действует до <pre>{subscriber.ended_at.strftime("%d.%m.%Y")}</pre>',
            reply_markup=subscribe_keyboard())
    else:
        await message.answer(
            text='🤖 Подписка дает возможность удобно скачивать любой контент из <pre>Instagram</pre>',
            reply_markup=subscribe_keyboard())


@dp.message_handler(text='💲 Подписка', state='*')
async def subscribe_message_handler(message: Message):
    subscriber = await Subscriber.add(user_id=message.chat.id, duration=0)
    if subscriber.is_actual():
        await message.answer(
            text=f'🤖 Твоя подписка действует до <pre>{subscriber.ended_at.strftime("%d.%m.%Y")}</pre>',
            reply_markup=subscribe_keyboard())
    else:
        await message.answer(
            text='🤖 Подписка дает возможность удобно скачивать любой контент из <pre>Instagram</pre>',
            reply_markup=subscribe_keyboard())


@dp.callback_query_handler(subscribe_callback.filter(), state='*')
async def subscribe_callback_query_handler(call: CallbackQuery, callback_data: dict):
    duration = int(callback_data['duration'])
    invoice_data = await get_invoice_data(user_id=call.from_user.id, duration=duration)
    redirected_url = await payment_link(targets=invoice_data['title'], price=invoice_data['price'],
                                        label=invoice_data['label'])
    await bot.send_message(chat_id=call.from_user.id,
                           text=f'<b>{invoice_data["title"]}</b>\n<i>{invoice_data["description"]}</i>',
                           reply_markup=payment_keyboard(url=str(redirected_url), price=invoice_data['price']))
