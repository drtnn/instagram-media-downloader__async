from aiogram.types import Message, InlineQuery
from loader import dp, bot, upload_client
from utils.db_api.database import Requests
from utils.instagram import InstagramHighlight


@dp.message_handler(is_subscriber=True, instagram_highlight=True, state='*')
async def instagram_highlight_handler(message: Message):
    post = InstagramHighlight(message.text)
    await post.start()
    await post.send_to(bot=bot, upload_client=upload_client, chat_id=message.chat.id)
    await Requests.add(user_id=message.from_user.id, content_type='h')


@dp.inline_handler(is_subscriber=True, instagram_inline_highlight=True, state='*')
async def instagram_highlight_inline_handler(query: InlineQuery):
    highlight = InstagramHighlight(query.query.strip())
    await highlight.start()
    await highlight.inline_to(query=query)
    await Requests.add(user_id=query.from_user.id, content_type='h')
