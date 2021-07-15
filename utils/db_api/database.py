from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup
from gino import Gino
from data.config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
import datetime
from sqlalchemy import Column, Integer, String, Sequence, DateTime, Boolean, Text, ForeignKey, Index
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


async def create_database():
    await database.set_bind(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
    try:
        await database.gino.create_all()
    except InvalidRequestError:
        pass
    return database
