duration_to_info = {
    14: {'title': '2 недели', 'price': 19},
    30: {'title': '1 месяц', 'price': 29},
    90: {'title': '3 месяца', 'price': 79},
}


def get_invoice_data(user_id: int, duration: int):
    return {
        'title': f'Подписка на {duration_to_info[duration]["title"]}',
        'description': f'Подписка дает возможность удобно скачивать любой контент из Instagram {duration_to_info[duration]["title"]}',
        'photo_url': 'https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/apple/285/camera-with-flash_1f4f8.png',
        'price': duration_to_info[duration]["price"],
        'label': f'{user_id}:{duration}',
    }
