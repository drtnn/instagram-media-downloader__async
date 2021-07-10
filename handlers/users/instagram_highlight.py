from aiogram.types import Message, InlineQuery
from loader import dp, bot, upload_client
from utils.instagram import InstagramHighlight


@dp.message_handler(instagram_highlight=True, state='*')
async def instagram_highlight_handler(message: Message):
    post = InstagramHighlight(message.text)
    await post.start()
    await post.send_to(bot=bot, upload_client=upload_client, chat_id=message.chat.id)


@dp.inline_handler(instagram_inline_highlight=True, state='*')
async def instagram_highlight_inline_handler(query: InlineQuery):
    highlight = InstagramHighlight(query.query.strip())
    await highlight.start()
    await highlight.inline_to(query=query)
