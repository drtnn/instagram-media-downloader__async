from aiogram.types import Message
from loader import dp, bot
from utils.db_api.database import User


@dp.channel_post_handler(chat_id=-1001558820128)
async def bot_resend_from_channel_to_users(message: Message):
    for user in await User.query.gino.all():
        await bot.forward_message(chat_id=user.user_id, from_chat_id=-1001558820128, message_id=message.message_id)
