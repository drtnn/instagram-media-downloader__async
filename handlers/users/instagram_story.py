from aiogram.types import Message, InlineQuery
from loader import dp, bot, upload_client
from utils.instagram import InstagramStory


@dp.message_handler(instagram_story=True, state='*')
async def instagram_story_handler(message: Message):
    post = InstagramStory(message.text)
    await post.start()
    await post.send_to(bot=bot, upload_client=upload_client, chat_id=message.chat.id)


@dp.inline_handler(instagram_inline_story=True, state='*')
async def instagram_story_inline_handler(query: InlineQuery):
    story = InstagramStory(query.query.strip())
    await story.start()
    await story.inline_to(query=query)
