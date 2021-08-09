from aiogram.types import Message
from keyboards.inline.generate import subscribe_keyboard
from loader import dp


@dp.message_handler(instagram_highlight=True, state='*')
async def not_instagram_highlight_handler(message: Message):
    await message.answer(
        text='🤖 Подключи подписку и скачивай контент из <pre>Instagram</pre> анонимно и без ограничений\nХочешь пользоваться ботом бесплатно? /referral\nХочешь подключить подписку? Кликай на кнопку ниже!',
        reply_markup=subscribe_keyboard())
