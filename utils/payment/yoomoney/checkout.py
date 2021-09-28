import asyncio
from data.config import YOOMONEY_TOKEN, ADMINS
from datetime import datetime, timedelta
from loader import bot
from utils.db_api.database import Purchase, Subscriber
from .client import Client


async def checkout(to_sleep: int = 10):
    client = Client(YOOMONEY_TOKEN)
    date = None
    while True:
        try:
            history = await client.operation_history(from_date=(date - timedelta(hours=12)) if date else None)
        except:
            continue
        date = datetime.now()
        for operation in history.operations:
            operation_data = operation.label.split(':') if operation.label else None
            if operation_data and len(operation_data) == 2:
                purc = await Purchase.get(user_id=int(operation_data[0]), amount=operation.amount,
                                          created_at=operation.datetime)
                if not purc:
                    await Purchase.add(user_id=int(operation_data[0]), amount=operation.amount,
                                       created_at=operation.datetime)
                    subscriber = await Subscriber.add(user_id=int(operation_data[0]), duration=int(operation_data[1]))
                    try:
                        await bot.send_message(chat_id=int(operation_data[0]),
                                               text=f'🤖 Подписка успешно оформлена и будет активна до <pre>{subscriber.ended_at.strftime("%d.%m.%Y")}</pre>')
                        await bot.send_message(chat_id=ADMINS[0], text=f'💸 +{operation.amount}₽')
                    except:
                        pass
        await asyncio.sleep(to_sleep)
