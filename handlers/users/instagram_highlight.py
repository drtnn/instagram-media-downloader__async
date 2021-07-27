from aiogram.types import Message, InlineQuery
from keyboards.inline.generate import subscribe_keyboard
from loader import dp, bot, upload_client
from utils.instagram import InstagramHighlight


@dp.message_handler(is_subscriber=True, instagram_highlight=True, state='*')
async def instagram_highlight_handler(message: Message):
    post = InstagramHighlight(message.text)
    await post.start()
    await post.send_to(bot=bot, upload_client=upload_client, chat_id=message.chat.id)


@dp.message_handler(instagram_highlight=True, state='*')
async def not_instagram_highlight_handler(message: Message):
    await message.answer(
        text='🤖 Подключи подписку и скачивай контент из <pre>Instagram</pre> анонимно и без ограничений\nХочешь пользоваться ботом бесплатно? /referral\nХочешь подключить подписку? Кликай на кнопку ниже!',
        reply_markup=subscribe_keyboard())


@dp.inline_handler(is_subscriber=True, instagram_inline_highlight=True, state='*')
async def instagram_highlight_inline_handler(query: InlineQuery):
    highlight = InstagramHighlight(query.query.strip())
    await highlight.start()
    await highlight.inline_to(query=query)
