from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup
from gino import Gino
from data.config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
import datetime
from sqlalchemy import Column, Integer, String, Sequence, DateTime, Boolean, Text, ForeignKey, Index, and_
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
            return new_user
        else:
            old_user.update(first_name=first_name, username=username)
            return old_user

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


class Item(database.Model):
    __tablename__ = 'items'

    id = Column(Integer, Sequence('item_id_seq'), primary_key=True)
    title = Column(String(64))
    description = Column(Text)
    photo = Column(String(256))
    price = Column(Integer)
    visible = Column(Boolean, default=True)
    query: sql.Select

    _idx = Index('item_id_index', 'id')

    def __init__(self, title: str = None, description: str = None, photo: str = None, price: int = None,
                 visible: bool = False):
        super().__init__()
        self.title, self.description, self.photo, self.price, self.visible = title, description, photo, price, visible

    def __repr__(self):
        return f'<Item(id=\'{self.id}\', name=\'{self.title}\', price=\'{self.price}\')>'


class Purchase(database.Model):
    __tablename__ = 'purchases'

    id = Column(Integer, Sequence('purc_id_seq'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    item_id = Column(Integer, ForeignKey('items.id'))
    amount = Column(Integer)
    purchase_time = Column(DateTime, server_default='now()')
    phone_number = Column(String(16))
    email = Column(String(128))
    receiver = Column(String(128))
    successful = Column(Boolean, default=False)
    query: sql.Select

    _idx = Index('purc_id_index', 'id')

    def __init__(self, user_id: int = None, item_id: int = None, amount: int = None,
                 purchase_time: datetime.datetime = None,
                 phone_number: str = None, email: str = None, receiver: str = None, successful: bool = False):
        super().__init__()
        self.user_id, self.item_id, self.amount, self.purchase_time, self.phone_number, self.email, self.receiver, self.successful = user_id, item_id, amount, purchase_time, phone_number, email, receiver, successful

    def __repr__(self):
        return f'<Purchase(id=\'{self.id}\', user_id=\'{self.user_id}\', amount=\'{self.amount}\')>'


class ParsedStory(database.Model):
    __tablename__ = 'parsed_stories'

    id = Column(Integer, Sequence('parsed_stories_id_seq'), primary_key=True)
    story_id = Column(String(32))
    parsed_date = Column(DateTime)
    query: sql.Select

    _idx1 = Index('parsed_stories_id_index', 'id')
    _idx2 = Index('story_id_index', 'story_id')

    def __init__(self, story_id: str = None, parsed_date: datetime.datetime = None):
        super().__init__()
        self.story_id, self.parsed_date = story_id, parsed_date

    def __repr__(self):
        return f'<ParsedStory(story_id=\'{self.story_id}\', parsed_date=\'{self.parsed_date.strftime("%d:%m:Y %H:%M")}\')>'

    @staticmethod
    async def delete_before(date: datetime.datetime):
        return await ParsedStory.delete.where(ParsedStory.parsed_date <= date).gino.status()


class Subscriber(database.Model):
    __tablename__ = 'subscribers'

    id = Column(Integer, Sequence('subscribers_id_seq'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    username_to_parse = Column(String())
    created_date = Column(DateTime)
    query: sql.Select

    _idx1 = Index('subscribers_id_index', 'id')
    _idx2 = Index('created_date_index', 'created_date')

    def __init__(self, user_id: int = None, username_to_parse: str = None, created_date: datetime.datetime = None):
        super().__init__()
        self.user_id, self.username_to_parse, self.created_date = user_id, username_to_parse, created_date

    def __repr__(self):
        return f'<Subscriber(user_id=\'{self.user_id}\', username_to_parse=\'{self.username_to_parse}\', created_date=\'{self.created_date.strftime("%d:%m:Y %H:%M")}\')>'

    @staticmethod
    async def get_actual_usernames(date: datetime.datetime):
        return await Subscriber.query.distinct(Subscriber.username_to_parse).where(
            Subscriber.created_date >= date).gino.all()

    @staticmethod
    async def get_user_ids(username: str, date: datetime.datetime):
        return await Subscriber.query.distinct(Subscriber.username_to_parse).where(
            and_(Subscriber.created_date >= date, Subscriber.username_to_parse == username)).gino.all()


async def create_database():
    await database.set_bind(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
    try:
        await database.gino.create_all()
    except InvalidRequestError:
        pass
