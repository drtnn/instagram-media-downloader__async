from aiogram.types import Message, InlineQuery
from loader import dp, bot, upload_client
from utils.db_api.database import Requests
from utils.instagram import InstagramStory


@dp.message_handler(is_subscriber=True, instagram_story=True, state='*')
async def instagram_story_handler(message: Message):
    post = InstagramStory(message.text)
    await post.start()
    await post.send_to(bot=bot, upload_client=upload_client, chat_id=message.chat.id)
    await Requests.add(user_id=message.from_user.id, content_type='s')


@dp.inline_handler(is_subscriber=True, instagram_inline_story=True, state='*')
async def instagram_story_inline_handler(query: InlineQuery):
    story = InstagramStory(query.query.strip())
    await story.start()
    await story.inline_to(query=query)
    await Requests.add(user_id=query.from_user.id, content_type='s')
