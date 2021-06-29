from aiogram.types import Message, CallbackQuery
from loader import dp, bot, upload_client
from keyboards.inline.callback_datas import stories_callback, posts_callback
from utils.instagram import InstagramUser


@dp.message_handler(content_types=['text'], instagram_user=True)
async def instagram_user_handler(message: Message):
    user = InstagramUser(message.text)
    await user.start()
    await user.send_to(bot=bot, chat_id=message.chat.id)


@dp.callback_query_handler(stories_callback.filter())
async def instagram_stories_callback_query_handler(call: CallbackQuery, callback_data: dict):
    user = InstagramUser(callback_data['username'])
    await user.start()
    await user.send_stories_to(bot=bot, upload_client=upload_client, chat_id=call.from_user.id, call=call)
