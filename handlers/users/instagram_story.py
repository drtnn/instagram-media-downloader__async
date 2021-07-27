from aiogram.types import Message, InlineQuery
from keyboards.inline.generate import subscribe_keyboard
from loader import dp, bot, upload_client
from utils.instagram import InstagramStory


@dp.message_handler(is_subscriber=True, instagram_story=True, state='*')
async def instagram_story_handler(message: Message):
    post = InstagramStory(message.text)
    await post.start()
    await post.send_to(bot=bot, upload_client=upload_client, chat_id=message.chat.id)


@dp.message_handler(instagram_story=True, state='*')
async def not_instagram_story_handler(message: Message):
    await message.answer(
        text='🤖 Подключи подписку и скачивай контент из <pre>Instagram</pre> анонимно и без ограничений\nХочешь пользоваться ботом бесплатно? /referral\nХочешь подключить подписку? Кликай на кнопку ниже!',
        reply_markup=subscribe_keyboard())


@dp.inline_handler(is_subscriber=True, instagram_inline_story=True, state='*')
async def instagram_story_inline_handler(query: InlineQuery):
    story = InstagramStory(query.query.strip())
    await story.start()
    await story.inline_to(query=query)
