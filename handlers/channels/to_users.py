from aiogram.types import Message
from aiogram.utils.exceptions import BotBlocked, MessageToForwardNotFound, MessageCantBeForwarded
from loader import dp
from utils.db_api.database import User


@dp.channel_post_handler(chat_id=-1001558820128)
async def bot_resend_to_users(message: Message):
    for user in await User.query.gino.all():
        try:
            await message.forward(chat_id=user.user_id)
        except (BotBlocked, MessageToForwardNotFound, MessageCantBeForwarded):
            pass
