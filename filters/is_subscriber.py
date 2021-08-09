from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter
from data.config import ADMINS
from utils.db_api.database import Subscriber


class SubscriberFilter(BoundFilter):
    key = 'is_subscriber'

    def __init__(self, is_subscriber):
        self.is_subscriber = is_subscriber

    async def check(self, message: Message):
        subscriber = await Subscriber.add(message.from_user.id, 0)
        return subscriber.is_actual() or message.from_user.id in ADMINS
