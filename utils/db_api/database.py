from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup
from gino import Gino
from data.config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, ADMINS
import datetime
from sqlalchemy import Column, Integer, String, Sequence, DateTime, ForeignKey, Index, and_
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy import sql

database = Gino()


class User(database.Model):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    user_id = Column(Integer, primary_key=True, unique=True)
    language = Column(String(2))
    first_name = Column(String(128))
    username = Column(String(128))
    referral = Column(Integer)
    query: sql.Select

    _idx = Index('user_id_index', 'user_id')

    def __init__(self, user_id: int = None, language: str = None, first_name: str = None, username: str = None,
                 referral: int = None):
        super().__init__()
        self.user_id, self.language, self.first_name, self.username, self.referral = user_id, language, first_name, username, referral

    async def set_language(self, language):
        await self.update(language=language).apply()

    @staticmethod
    async def get_user(user_id: int):
        return await User.query.where(User.user_id == user_id).gino.first()

    @staticmethod
    async def add_user(user_id: int, language: str = None, first_name: str = None, username: str = None,
                       referral: int = None):
        old_user = await User.get_user(user_id=user_id)
        if not old_user:
            new_user = User(user_id=user_id, language=language, first_name=first_name, username=username,
                            referral=referral)
            await new_user.create()
            return new_user, False
        else:
            old_user.update(first_name=first_name, username=username)
            return old_user, True

    @staticmethod
    async def mailing(bot: Bot, text: str, keyboard: InlineKeyboardMarkup = None) -> int:
        count_users = 0
        for user in await User.query.gino.all():
            try:
                await bot.send_message(chat_id=user.user_id, text=text, reply_markup=keyboard)
                count_users += 1
            except:
                pass
        return count_users

    @staticmethod
    async def count_users() -> int:
        return await database.func.count(User.id).gino.scalar()

    def __repr__(self):
        return f'<User(id=\'{self.id}\', first_name=\'{self.first_name}\', username=\'{self.username}\')>'


class Purchase(database.Model):
    __tablename__ = 'purchases'

    id = Column(Integer, Sequence('purc_id_seq'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    amount = Column(Integer)
    purchase_time = Column(DateTime, server_default='now()')
    query: sql.Select

    _idx = Index('purc_id_index', 'id')

    def __init__(self, user_id: int = None, amount: int = None):
        super().__init__()
        self.user_id, self.amount, self.purchase_time = user_id, amount, datetime.datetime.now()

    def __repr__(self):
        return f'<Purchase(id=\'{self.id}\', user_id=\'{self.user_id}\', amount=\'{self.amount}\')>'


class ParsedStory(database.Model):
    __tablename__ = 'parsed_stories'

    id = Column(Integer, Sequence('parsed_stories_id_seq'), primary_key=True)
    story_id = Column(String(32))
    parsed_date = Column(DateTime)
    query: sql.Select

    _idx1 = Index('parsed_stories_id_index', 'id')
    _idx2 = Index('parsed_stories_story_id_index', 'story_id')

    def __init__(self, story_id: str = None):
        super().__init__()
        self.story_id, self.parsed_date = story_id, datetime.datetime.now()

    def __repr__(self):
        return f'<ParsedStory(story_id=\'{self.story_id}\', parsed_date=\'{self.parsed_date.strftime("%d:%m:Y %H:%M")}\')>'

    @staticmethod
    async def delete_before(date: datetime.datetime):
        return await ParsedStory.delete.where(ParsedStory.parsed_date <= date).gino.status()


class Subscriber(database.Model):
    __tablename__ = 'subscribers'

    id = Column(Integer, Sequence('subscribers_id_seq'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    subs_limit = Column(Integer)
    query: sql.Select

    _idx1 = Index('subscribers_id_index', 'id')
    _idx2 = Index('subscribers_user_id_index', 'user_id')

    def __init__(self, user_id: int = None, subs_limit: int = None):
        super().__init__()
        self.user_id, self.subs_limit = user_id, subs_limit

    async def add_subs(self, subs: int):
        await self.update(subs_limit=self.subs_limit + subs).apply()

    async def subscribe(self, username: str):
        if self.user_id not in ADMINS:
            await self.update(subs_limit=self.subs_limit - 1).apply()
        subscription = Subscription(user_id=self.user_id, username_to_parse=username)
        await subscription.create()
        return subscription

    @staticmethod
    async def add(user_id: int, subs: int):
        subscriber = await Subscriber.query.where(Subscriber.user_id == user_id).gino.first()
        if subscriber:
            await subscriber.add_subs(subs)
        else:
            subscriber = Subscriber(user_id=user_id, subs_limit=subs)
            await subscriber.create()
        return subscriber

    @staticmethod
    async def get(user_id: int):
        return await Subscriber.query.where(Subscriber.user_id == user_id).gino.first()

    def __repr__(self):
        return f'<Subscriber(user_id=\'{self.user_id}\', subs_limit=\'{self.limited_subs}\')>'


class Subscription(database.Model):
    __tablename__ = 'subscriptions'

    id = Column(Integer, Sequence('subscriptions_id_seq'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    username_to_parse = Column(String())
    created_date = Column(DateTime)
    query: sql.Select

    _idx1 = Index('subscriptions_id_index', 'id')
    _idx2 = Index('subscriptions_user_id_index', 'user_id')
    _idx3 = Index('subscriptions_created_date_index', 'created_date')

    def __init__(self, user_id: int = None, username_to_parse: str = None):
        super().__init__()
        self.user_id, self.username_to_parse, self.created_date = user_id, username_to_parse, datetime.datetime.now()

    def __repr__(self):
        return f'<Subscription(user_id=\'{self.user_id}\', username_to_parse=\'{self.username_to_parse}\', created_date=\'{self.created_date.strftime("%d:%m:Y %H:%M")}\')>'

    @staticmethod
    async def get_actual_usernames():
        return await Subscription.query.distinct(Subscription.username_to_parse).where(
            Subscription.created_date >= datetime.datetime.now() - datetime.timedelta(30)).gino.all()

    @staticmethod
    async def get_user_ids(username: str):
        return await Subscription.query.distinct(Subscription.username_to_parse).where(
            and_(Subscription.created_date >= datetime.datetime.now() - datetime.timedelta(30),
                 Subscription.username_to_parse == username)).gino.all()

    @staticmethod
    async def exists(user_id: int, username: str):
        return True if await Subscription.query.where(
            and_(Subscription.user_id == user_id, Subscription.username_to_parse == username,
                 Subscription.created_date >= datetime.datetime.now() - datetime.timedelta(30))).gino.first() else False


async def create_database():
    await database.set_bind(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
    try:
        await database.gino.create_all()
    except InvalidRequestError:
        pass
