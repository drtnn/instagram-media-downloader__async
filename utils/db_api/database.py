from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup
from asyncpg.exceptions import ForeignKeyViolationError
from gino import Gino
from data.config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, ADMINS
import datetime
from sqlalchemy import Column, Integer, String, Sequence, DateTime, ForeignKey, Index, and_, Float
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
            await old_user.update(first_name=first_name, username=username).apply()
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
    amount = Column(Float)
    purchase_time = Column(DateTime, server_default='now()')
    query: sql.Select

    _idx = Index('purc_id_index', 'id')

    def __init__(self, user_id: int = None, amount: int = None,
                 purchase_time: datetime.datetime = datetime.datetime.now()):
        super().__init__()
        self.user_id, self.amount, self.purchase_time = user_id, amount, purchase_time

    async def payed(self):
        await self.update(successful=True).apply()

    @staticmethod
    async def get(user_id: int, amount: int, purchase_time: datetime.datetime):
        return await Purchase.query.where(and_(and_(Purchase.user_id == user_id, Purchase.amount == amount),
                                               Purchase.purchase_time == purchase_time)).gino.first()

    def __repr__(self):
        return f'<Purchase(id=\'{self.id}\', user_id=\'{self.user_id}\', amount=\'{self.amount}\')>'


class Subscriber(database.Model):
    __tablename__ = 'subscribers'

    id = Column(Integer, Sequence('subscribers_id_seq'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    ended_at = Column(DateTime)
    query: sql.Select

    _idx1 = Index('subscribers_id_index', 'id')
    _idx2 = Index('subscribers_user_id_index', 'user_id')

    def __init__(self, user_id: int = None, ended_at: datetime.datetime = None):
        super().__init__()
        self.user_id, self.ended_at = user_id, ended_at

    @staticmethod
    async def add(user_id: int, duration: int):
        subscriber = await Subscriber.get(user_id=user_id)
        if subscriber and subscriber.is_actual():
            await subscriber.update(ended_at=subscriber.ended_at + datetime.timedelta(duration)).apply()
        elif subscriber:
            await subscriber.update(ended_at=datetime.datetime.now() + datetime.timedelta(duration)).apply()
        else:
            try:
                subscriber = Subscriber(user_id=user_id, ended_at=datetime.datetime.now() + datetime.timedelta(duration))
                await subscriber.create()
            except ForeignKeyViolationError:
                await User.add_user(user_id=user_id)
                subscriber = Subscriber(user_id=user_id, ended_at=datetime.datetime.now() + datetime.timedelta(duration))
                await subscriber.create()
        return subscriber

    def is_actual(self):
        return True if self.ended_at >= datetime.datetime.now() else False

    @staticmethod
    async def get(user_id: int):
        return await Subscriber.query.where(Subscriber.user_id == user_id).gino.first()

    def __repr__(self):
        return f'<Subscriber(user_id=\'{self.user_id}\', subs_limit=\'{self.limited_subs}\')>'


async def create_database():
    await database.set_bind(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
    try:
        await database.gino.create_all()
    except InvalidRequestError:
        pass
