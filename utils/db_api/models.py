from gino import Gino
from sqlalchemy import Column, Integer, String, Sequence, DateTime, Boolean, Text
from sqlalchemy import sql

database = Gino()


class User(database.Model):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    user_id = Column(Integer)
    language = Column(String(2))
    first_name = Column(String(128))
    username = Column(String(128))
    referral = Column(Integer)
    query: sql.Select

    def __init__(self, user_id: int, language: str = None, first_name: str = None, username: str = None,
                 referral: int = None):
        self.user_id, self.language, self.first_name, self.username, self.referral = user_id, language, first_name, username, referral

    @classmethod
    async def get_user(cls, user_id):
        user = await cls.query.where(cls.user_id == user_id).gino.first()
        return user

    @classmethod
    async def add_user(cls, user_id: int, language: str = None, first_name: str = None, username: str = None,
                       referral: int = None):
        old_user = await cls.get_user(user_id)
        if not old_user:
            new_user = User(user_id=user_id, language=language, first_name=first_name, username=username,
                            referral=referral)
            await new_user.create()
            return new_user
        else:
            old_user.update(first_name=first_name, username=username)
            return old_user

    async def set_language(self, language):
        await self.update(language=language).apply()

    @classmethod
    async def count_users(cls) -> int:
        total = await database.func.count(cls.id).gino.scalar()
        return total

    def __repr__(self):
        return "<User(id='{}', first_name='{}', username='{}')>".format(
            self.id, self.first_name, self.username)


class Item(database.Model):
    __tablename__ = 'items'

    id = Column(Integer, Sequence('item_id_seq'), primary_key=True)
    name = Column(String(64))
    description = Column(Text)
    photo = Column(String(256))
    price = Column(Integer)
    query: sql.Select

    def __repr__(self):
        return "<Item(id='{}', name='{}', price='{}')>".format(
            self.id, self.name, self.price)


class Purchase(database.Model):
    __tablename__ = 'purchases'
    query: sql.Select

    id = Column(Integer, Sequence('purc_id_seq'), primary_key=True)
    buyer = Column(BigInteger)
    item_id = Column(Integer)
    amount = Column(Integer)  # Цена в копейках (потом делим на 100)
    quantity = Column(Integer)
    purschase_time = Column(TIMESTAMP)
    shipping_address = Column(JSON)
    phone_number = Column(String(50))
    email = Column(String(200))
    receiver = Column(String(100))
    successful = Column(Boolean, default=False)
