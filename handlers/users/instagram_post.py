from aiogram.types import Message, InlineQuery
from keyboards.inline.generate import subscribe_keyboard
from loader import dp, bot, upload_client
from utils.instagram import InstagramPost


@dp.message_handler(is_subscriber=True, instagram_post=True, state='*')
async def instagram_post_handler(message: Message):
    post = InstagramPost(message.text)
    await post.start()
    await post.send_to(bot=bot, upload_client=upload_client, chat_id=message.chat.id)


@dp.message_handler(instagram_post=True, state='*')
async def not_instagram_post_handler(message: Message):
    await message.answer(
        text='🤖 Подключи подписку и скачивай контент из <pre>Instagram</pre> анонимно и без ограничений\nХочешь пользоваться ботом бесплатно? /referral\nХочешь подключить подписку? Кликай на кнопку ниже!',
        reply_markup=subscribe_keyboard())


@dp.inline_handler(is_subscriber=True, instagram_inline_post=True, state='*')
async def instagram_post_inline_handler(query: InlineQuery):
    post = InstagramPost(query.query.strip())
    await post.start()
    await post.inline_to(query=query)
