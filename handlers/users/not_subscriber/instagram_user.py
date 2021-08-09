from aiogram.types import Message, CallbackQuery
from keyboards.inline.generate import subscribe_keyboard
from loader import dp, bot
from keyboards.inline.callback_datas import stories_callback
from utils.instagram import InstagramUser


@dp.message_handler(instagram_user=True, state='*')
async def not_instagram_user_handler(message: Message):
    user = InstagramUser(message.text.lower())
    await user.start()
    await user.send_to(bot=bot, chat_id=message.chat.id, posts_button=False)


@dp.callback_query_handler(stories_callback.filter(), state='*')
async def not_instagram_stories_callback_query_handler(call: CallbackQuery, callback_data: dict):
    await bot.send_message(chat_id=call.from_user.id,
                           text='🤖 Подключи подписку и скачивай контент из <pre>Instagram</pre> анонимно и без ограничений\nХочешь пользоваться ботом бесплатно? /referral\nХочешь подключить подписку? Кликай на кнопку ниже!',
                           reply_markup=subscribe_keyboard())
