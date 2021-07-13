from data.config import DATABASE_URL
from models import database


async def create_database():
    await database.set_bind(DATABASE_URL)
    await database.gino.create_all()
