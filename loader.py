from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from data.config import BOT_TOKEN, TELETHON_SESSION, TELETHON_API_ID, TELETHON_API_HASH
from utils.upload_client import UploadClient

loop = asyncio.get_event_loop()
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

upload_client = loop.run_until_complete(UploadClient(TELETHON_SESSION, TELETHON_API_ID, TELETHON_API_HASH).start())
