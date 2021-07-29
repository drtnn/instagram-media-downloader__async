from datetime import timedelta
from utils.db_api.database import Subscriber

duration_to_info = {
    14: {'title': '2 недели', 'price': 19, 'emoji': '💳'},
    30: {'title': '1 месяц', 'price': 29, 'emoji': '💸'},
    90: {'title': '3 месяца', 'price': 79, 'emoji': '💰'},
}


def get_invoice_data(user_id: int, duration: int):
    subscriber = await Subscriber.add(user_id=user_id, duration=0)
    ended_at = subscriber.ended_at + timedelta(duration)
    return {
        'title': f'{duration_to_info[duration]["emoji"]} Подписка на {duration_to_info[duration]["title"]}',
        'description': f'Подписка дает возможность удобно скачивать любой контент из Instagram и продлится до {ended_at.strftime("%d.%m.%Y")}',
        'price': duration_to_info[duration]["price"],
        'label': f'{user_id}:{duration}',
    }
