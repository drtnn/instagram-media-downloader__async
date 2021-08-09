from aiogram.types import InlineQueryResultArticle, InputTextMessageContent


def inline_no_such_user():
    return [
        InlineQueryResultArticle(
            id='inline_no_such_user',
            title='Профиль закрыт или не существует',
            description='Мне не удалось получить данные о профиле из Instagram',
            input_message_content=InputTextMessageContent(
                message_text=f'Переходи в <b>@InstagramMediaDownloadBot</b> и скачивай контент из Instagram!',
                parse_mode='html'
            ),
            thumb_url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/271/videocassette_1f4fc.png',
            thumb_width=48,
            thumb_height=48
        )
    ]


def inline_no_actual_stories():
    return [
        InlineQueryResultArticle(
            id='inline_no_actual_stories',
            title='Нет актуальных историй',
            description='Мне не удалось получить данные об актуальных историях из Instagram',
            input_message_content=InputTextMessageContent(
                message_text=f'Переходи в <b>@InstagramMediaDownloadBot</b> и скачивай контент из Instagram!',
                parse_mode='html'
            ),
            thumb_url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/271/videocassette_1f4fc.png',
            thumb_width=48,
            thumb_height=48
        )
    ]


def inline_no_actual_posts():
    return [
        InlineQueryResultArticle(
            id='inline_no_actual_posts',
            title='Нет актуальных постов',
            description='Мне не удалось получить данные о существующих постах из Instagram',
            input_message_content=InputTextMessageContent(
                message_text=f'Переходи в <b>@InstagramMediaDownloadBot</b> и скачивай контент из Instagram!',
                parse_mode='html'
            ),
            thumb_url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/271/videocassette_1f4fc.png',
            thumb_width=48,
            thumb_height=48
        )
    ]


def inline_no_such_media(media_type: str):
    return [
        InlineQueryResultArticle(
            id='inline_no_such_media',
            title=f'{media_type} не найден или не существует',
            description='Мне не удалось получить данные из Instagram',
            input_message_content=InputTextMessageContent(
                message_text=f'Переходи в <b>@InstagramMediaDownloadBot</b> и скачивай контент из Instagram!',
                parse_mode='html'
            ),
            thumb_url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/271/videocassette_1f4fc.png',
            thumb_width=48,
            thumb_height=48
        )
    ]


def inline_start():
    return [
        InlineQueryResultArticle(
            id='inline_start',
            title='Привет, это мой инлайн-режим',
            description='Вставь ссылку на пост, историю, хайлайт или никнейм',
            input_message_content=InputTextMessageContent(
                message_text=f'Переходи в <b>@InstagramMediaDownloadBot</b> и скачивай контент из Instagram!',
                parse_mode='html'
            ),
            thumb_url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/320/apple/285/man-raising-hand-light-skin-tone_1f64b-1f3fb-200d-2642-fe0f.png',
            thumb_width=48,
            thumb_height=48
        )
    ]


def not_inline_start():
    return [
        InlineQueryResultArticle(
            id='not_inline_start',
            title='Привет, это мой инлайн-режим',
            description='Для работы в инлайн режиме нужно приобрети подписку – /subscribe',
            input_message_content=InputTextMessageContent(
                message_text=f'Переходи в <b>@InstagramMediaDownloadBot</b> и скачивай контент из Instagram!',
                parse_mode='html'
            ),
            thumb_url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/320/apple/285/man-raising-hand-light-skin-tone_1f64b-1f3fb-200d-2642-fe0f.png',
            thumb_width=48,
            thumb_height=48
        )
    ]
