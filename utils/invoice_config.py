from aiogram.types import LabeledPrice
from data.config import PROVIDER_TOKEN

accounts_count_to_amount = {
    3: 2900,
    5: 4900,
    10: 8900
}


def get_invoice_data(username: str, accounts_count: int):
    return {
        'title': f'Подписка на контент',
        'description': f'Подписка дает возможность получать истории {accounts_count} публичных аккаунта(ов) на 1 месяц',
        'provider_token': PROVIDER_TOKEN, 'currency': 'rub',
        'photo_url': 'https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/apple/285/camera-with-flash_1f4f8.png',
        'photo_size': 160, 'photo_width': 160, 'photo_height': 160, 'is_flexible': False,
        'prices': [LabeledPrice(label=f'Месячная подписка на {accounts_count} аккаунта(ов)',
                                amount=accounts_count_to_amount[accounts_count])],
        'start_parameter': 'instagram-stories-subscribe',
        'payload': f'subscribe:{accounts_count}:{username}',
    }
