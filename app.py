from aiogram import executor
import asyncio
from loader import dp, upload_client, bot
import middlewares, filters, handlers
from utils.db_api.database import create_database
from utils.instagram import ScheduledParser
from utils.notify_admins import on_startup_notify, on_shutdown_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    await create_database()
    await upload_client.start()
    loop = asyncio.get_event_loop()
    loop.create_task(ScheduledParser(bot=bot, upload_client=upload_client).start())

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown_notify)
