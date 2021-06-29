from aiogram.types import Message
from loader import dp, bot, upload_client
from utils.instagram import InstagramHighlight


@dp.message_handler(content_types=['text'], instagram_highlight=True)
async def instagram_user_handler(message: Message):
    post = InstagramHighlight(message.text)
    await post.start()
    await post.send_to(bot=bot, upload_client=upload_client, chat_id=message.chat.id)
