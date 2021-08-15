from aiogram.types import Message, InlineQuery
from loader import dp, bot, upload_client
from utils.db_api.database import Requests
from utils.instagram import InstagramPost


@dp.message_handler(is_subscriber=True, instagram_post=True, state='*')
async def instagram_post_handler(message: Message):
    post = InstagramPost(message.text)
    await post.start()
    await post.send_to(bot=bot, upload_client=upload_client, chat_id=message.chat.id)
    await Requests.add(user_id=message.from_user.id, content_type='p')


@dp.inline_handler(is_subscriber=True, instagram_inline_post=True, state='*')
async def instagram_post_inline_handler(query: InlineQuery):
    post = InstagramPost(query.query.strip())
    await post.start()
    await post.inline_to(query=query)
    await Requests.add(user_id=query.from_user.id, content_type='p')
