from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.exceptions import BotBlocked
from gino import Gino
from data.config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, Sequence, DateTime, ForeignKey, Index, and_, VARCHAR
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
    created_at = Column(DateTime)
    query: sql.Select

    _idx = Index('user_id_index', 'user_id')

    def __init__(self, user_id: int = None, language: str = None, first_name: str = None, username: str = None,
                 referral: int = None, created_at: datetime = datetime.now()):
        super().__init__()
        self.user_id, self.language, self.first_name, self.username, self.referral, self.created_at = user_id, language, first_name, username, referral, created_at

    async def set_language(self, language):
        await self.update(language=language).apply()

    @staticmethod
    async def get(user_id: int):
        return await User.query.where(User.user_id == user_id).gino.first()

    @staticmethod
    async def add(user_id: int, language: str = None, first_name: str = None, username: str = None,
                  referral: int = None):
        old_user = await User.get(user_id=user_id)
        if not old_user:
            new_user = User(user_id=user_id, language=language, first_name=first_name, username=username,
                            referral=referral, created_at=datetime.now())
            await new_user.create()
            return new_user, False
        else:
            return old_user, True

    @staticmethod
    async def mailing(bot: Bot, text: str, keyboard: InlineKeyboardMarkup = None) -> int:
        count_users = 0
        for user in await User.query.gino.all():
            try:
                await bot.send_message(chat_id=user.user_id, text=text, reply_markup=keyboard)
                count_users += 1
            except BotBlocked:
                pass
        return count_users

    @staticmethod
    async def count_users() -> int:
        return await database.func.count(User.id).gino.scalar()

    @staticmethod
    async def count_for_date(date: datetime):
        next_day = date.date() + timedelta(1)
        return await database.select([database.func.count()]).where(
            and_(User.created_at >= date.date(), User.created_at < next_day)).gino.scalar()

    @staticmethod
    async def count_for_dates(date: datetime, duration: int):
        result = dict()
        for day in reversed(range(duration)):
            tmp_date = date - timedelta(day)
            result[tmp_date.strftime('%d.%m')] = await User.count_for_date(tmp_date)
        return result

    def __repr__(self):
        return f'<User(id=\'{self.id}\', first_name=\'{self.first_name}\', username=\'{self.username}\')>'


class Requests(database.Model):
    __tablename__ = 'requests'

    id = Column(Integer, Sequence('requests_users_id_seq'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    created_at = Column(DateTime)
    content_type = Column(VARCHAR(length=1))
    query: sql.Select

    _idx1 = Index('requests_id_index', 'id')
    _idx2 = Index('requests_user_id_index', 'user_id')
    _idx3 = Index('requests_created_at_index', 'created_at')
    _idx4 = Index('requests_content_type_index', 'content_type')

    def __init__(self, user_id: int = None, content_type: str = None, created_at: datetime = datetime.now()):
        super().__init__()
        self.user_id, self.content_type, self.created_at = user_id, content_type, created_at

    @staticmethod
    async def add(user_id: int, content_type: str):
        user, _ = await User.add(user_id=user_id)
        requests = Requests(user_id=user_id, content_type=content_type, created_at=datetime.now())
        await requests.create()
        return requests

    @staticmethod
    async def count_for_date(date: datetime):
        next_day = date.date() + timedelta(1)
        return await database.select([database.func.count()]).where(
            and_(Requests.created_at >= date.date(), Requests.created_at < next_day)).gino.scalar()

    @staticmethod
    async def count_for_dates(date: datetime, duration: int):
        result = dict()
        for day in reversed(range(duration)):
            tmp_date = date - timedelta(day)
            result[tmp_date.strftime('%d.%m')] = await Requests.count_for_date(tmp_date)
        return result

    @staticmethod
    async def count_of_content_type(content_type: str, date: datetime = None, duration: int = None):
        if date and duration:
            first_date = date.date() - timedelta(duration)
            return await database.select([database.func.count()]).where(
                and_(and_(Requests.created_at >= first_date, Requests.created_at <= date.date()),
                     Requests.content_type == content_type)).gino.scalar()
        else:
            return await database.select([database.func.count()]).where(
                Requests.content_type == content_type).gino.scalar()

    def __repr__(self):
        return f'<Requests(user_id=\'{self.user_id}\', created_at=\'{self.created_at.strftime("%d.%m.%Y")}\')>'


async def create_database():
    await database.set_bind(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
    try:
        await database.gino.create_all()
    except InvalidRequestError:
        pass
