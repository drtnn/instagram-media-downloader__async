from aiogram.types import LabeledPrice
from data.config import PROVIDER_TOKEN

duration_to_info = {
    14: {'amount': 1900, 'title': '2 недели', 'price': 19},
    30: {'amount': 2900, 'title': '1 месяц', 'price': 29},
    90: {'amount': 7900, 'title': '3 месяца', 'price': 79},
}


def get_invoice_data(duration: int):
    return {
        'title': f'Подписка на {duration_to_info[duration]["title"]}',
        'description': f'Подписка дает возможность удобно скачивать любой контент из Instagram {duration_to_info[duration]["title"]}',
        'provider_token': PROVIDER_TOKEN, 'currency': 'rub',
        'photo_url': 'https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/apple/285/camera-with-flash_1f4f8.png',
        'photo_size': 160, 'photo_width': 160, 'photo_height': 160, 'is_flexible': False,
        'prices': [LabeledPrice(label=f'Подписка на {duration_to_info[duration]["title"]}',
                                amount=duration_to_info[duration]['amount'])],
        'start_parameter': 'instagram-bot-subscribe',
        'payload': f'subscribe:{duration}',
    }
