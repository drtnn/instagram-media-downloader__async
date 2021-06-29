from aiogram.types import Message
from loader import dp, bot, upload_client
from utils.instagram import InstagramPost


@dp.message_handler(content_types=['text'], instagram_post=True)
async def instagram_user_handler(message: Message):
    post = InstagramPost(message.text)
    await post.start()
    await post.send_to(bot=bot, upload_client=upload_client, chat_id=message.chat.id)
