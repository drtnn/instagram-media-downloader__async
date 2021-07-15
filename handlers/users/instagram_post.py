from aiogram.types import Message, InlineQuery
from loader import dp, bot, upload_client
from utils.instagram import InstagramPost


@dp.message_handler(instagram_post=True, state='*')
async def instagram_post_handler(message: Message):
    post = InstagramPost(message.text)
    await post.start()
    await post.send_to(bot=bot, upload_client=upload_client, chat_id=message.chat.id)


@dp.inline_handler(instagram_inline_post=True, state='*')
async def instagram_post_inline_handler(query: InlineQuery):
    post = InstagramPost(query.query.strip())
    await post.start()
    await post.inline_to(query=query)
