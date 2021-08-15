from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.exceptions import BotBlocked
from asyncpg.exceptions import ForeignKeyViolationError
from gino import Gino
from data.config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, Sequence, DateTime, ForeignKey, Index, and_, Float, Boolean
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
    created_at = Column(DateTime, default=datetime.now())
    query: sql.Select

    _idx = Index('user_id_index', 'user_id')

    def __init__(self, user_id: int = None, language: str = None, first_name: str = None, username: str = None,
                 referral: int = None):
        super().__init__()
        self.user_id, self.language, self.first_name, self.username, self.referral = user_id, language, first_name, username, referral

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
                            referral=referral)
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
            and_(User.created_at >= date.date(), User.created_at <= next_day)).gino.scalar()

    @staticmethod
    async def count_for_dates(date: datetime, duration: int):
        result = dict()
        for day in reversed(range(duration)):
            tmp_date = date - timedelta(day)
            result[tmp_date.strftime('%d.%m')] = await User.count_for_date(tmp_date)
        return result

    def __repr__(self):
        return f'<User(id=\'{self.id}\', first_name=\'{self.first_name}\', username=\'{self.username}\')>'


class Purchase(database.Model):
    __tablename__ = 'purchases'

    id = Column(Integer, Sequence('purc_id_seq'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    amount = Column(Float)
    purchase_time = Column(DateTime, default=datetime.now())
    query: sql.Select

    _idx = Index('purc_id_index', 'id')

    def __init__(self, user_id: int = None, amount: int = None,
                 purchase_time: datetime = None):
        super().__init__()
        self.user_id, self.amount, self.purchase_time = user_id, amount, purchase_time

    @staticmethod
    async def add(user_id: int = None, amount: int = None,
                  purchase_time: datetime = None):
        try:
            purc = Purchase(user_id, amount, purchase_time)
            await purc.create()
        except ForeignKeyViolationError:
            await User.add(user_id=user_id)
            purc = Purchase(user_id, amount, purchase_time)
            await purc.create()
        return purc

    @staticmethod
    async def get(user_id: int, amount: int, purchase_time: datetime):
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

    def __init__(self, user_id: int = None, ended_at: datetime = None):
        super().__init__()
        self.user_id, self.ended_at = user_id, ended_at

    @staticmethod
    async def add(user_id: int, duration: int):
        subscriber = await Subscriber.get(user_id=user_id)
        if subscriber and subscriber.is_actual():
            await subscriber.update(ended_at=subscriber.ended_at + timedelta(duration)).apply()
        elif subscriber:
            await subscriber.update(ended_at=datetime.now() + timedelta(duration)).apply()
        else:
            try:
                subscriber = Subscriber(user_id=user_id,
                                        ended_at=datetime.now() + timedelta(duration))
                await subscriber.create()
            except ForeignKeyViolationError:
                await User.add(user_id=user_id)
                subscriber = Subscriber(user_id=user_id,
                                        ended_at=datetime.now() + timedelta(duration))
                await subscriber.create()
        return subscriber

    def is_actual(self):
        return True if self.ended_at >= datetime.now() else False

    @staticmethod
    async def get(user_id: int):
        return await Subscriber.query.where(Subscriber.user_id == user_id).gino.first()

    def __repr__(self):
        return f'<Subscriber(user_id=\'{self.user_id}\', ended_at=\'{self.ended_at.strftime("%d.%m.%Y")}\')>'


class Giveaway(database.Model):
    __tablename__ = 'giveaways'

    id = Column(Integer, Sequence('giveaways_id_seq'), primary_key=True)
    created_at = Column(DateTime, default=datetime.now())
    query: sql.Select

    _idx1 = Index('giveaways_id_index', 'id')

    @staticmethod
    async def add():
        giveaway = Giveaway()
        await giveaway.create()
        return giveaway

    def __repr__(self):
        return f'<Giveaway(id=\'{self.id}\')>'


class GiveawayUser(database.Model):
    __tablename__ = 'giveaway_users'

    id = Column(Integer, Sequence('giveaway_users_id_seq'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    created_at = Column(DateTime, default=datetime.now())
    giveaway_id = Column(Integer, ForeignKey('giveaways.id'))
    query: sql.Select

    _idx1 = Index('giveaway_users_id_index', 'id')
    _idx2 = Index('giveaway_users_user_id_index', 'user_id')

    def __init__(self, user_id: int = None, giveaway_id: int = None):
        super().__init__()
        self.user_id, self.giveaway_id = user_id, giveaway_id

    @staticmethod
    async def add(user_id: int, giveaway_id: int):
        giveaway_user = await GiveawayUser.get(user_id=user_id, giveaway_id=giveaway_id)
        if giveaway_user:
            return giveaway_user, True
        else:
            try:
                giveaway_user = GiveawayUser(user_id=user_id, giveaway_id=giveaway_id)
                await giveaway_user.create()
                return giveaway_user, False
            except ForeignKeyViolationError:
                return None

    @staticmethod
    async def get(user_id: int, giveaway_id: int):
        return await GiveawayUser.query.where(
            and_(GiveawayUser.user_id == user_id, GiveawayUser.giveaway_id == giveaway_id)).gino.first()

    def __repr__(self):
        return f'<GiveawayUser(user_id=\'{self.user_id}\', giveaway_id=\'{self.giveaway_id}\')>'


class RequestsAnalytic(database.Model):
    __tablename__ = 'requests_analytic'

    id = Column(Integer, Sequence('giveaway_users_id_seq'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    created_at = Column(DateTime, default=datetime.now())
    from_subscriber = Column(Boolean)
    query: sql.Select

    _idx1 = Index('requests_analytic_id_index', 'id')
    _idx2 = Index('requests_analytic_user_id_index', 'user_id')
    _idx3 = Index('requests_analytic_created_at_index', 'created_at')

    def __init__(self, user_id: int = None, from_subscriber: bool = None):
        super().__init__()
        self.user_id, self.from_subscriber = user_id, from_subscriber

    @staticmethod
    async def add(user_id: int):
        subscriber = await Subscriber.add(user_id=user_id, duration=0)
        requests_analytic = RequestsAnalytic(user_id=user_id, from_subscriber=subscriber.is_actual())
        await requests_analytic.create()
        return requests_analytic

    def __repr__(self):
        return f'<RequestsAnalytic(user_id=\'{self.user_id}\', created_at=\'{self.created_at.strftime("%d.%m.%Y")}\')>'


async def create_database():
    await database.set_bind(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
    try:
        await database.gino.create_all()
    except InvalidRequestError:
        pass
