import asyncio
import asyncpg
from data.config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
import logging


async def create_db():
    create_db_command = open("create_db.sql", "r").read()

    logging.info("Connecting to database...")
    conn: asyncpg.Connection = await asyncpg.connect(user=DB_USER,
                                                     password=DB_PASSWORD,
                                                     host=DB_HOST, port=DB_PORT)
    await conn.execute(create_db_command)
    await conn.close()
    logging.info("Table users created")


async def create_pool():
    return await asyncpg.create_pool(user=DB_USER,
                                     password=DB_PASSWORD,
                                     host=DB_HOST, port=DB_PORT)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_db())
