from aiogram import executor
import asyncio
from loader import dp, upload_client
import middlewares, filters, handlers
from utils.db_api.database import create_database
from utils.payment.yoomoney.checkout import checkout
from utils.notify_admins import on_startup_notify, on_shutdown_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_database())
    loop.run_until_complete(upload_client.start())
    loop.create_task(checkout())
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown_notify)
