from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .callback_datas import stories_callback, subscribe_callback, mutable_subscribe_callback


def user_keyboard(username: str, is_private: bool, is_subscribed: bool, posts_button: bool = True):
    keyboard = InlineKeyboardMarkup(row_width=1)
    instagram_link = InlineKeyboardButton(text='📸 Instagram', url=f'https://www.instagram.com/{username}')
    if not is_private:
        stories_button = InlineKeyboardButton(text='📹 Истории', callback_data=stories_callback.new(username=username))
        if posts_button:
            posts_button = InlineKeyboardButton(text='📽 Посты', switch_inline_query_current_chat='')
            keyboard.row(stories_button, posts_button)
        else:
            keyboard.add(stories_button)
        keyboard.add(instagram_link)
        if not is_subscribed:
            subscribe_button = InlineKeyboardButton(text='💳 Подписаться',
                                                    callback_data=subscribe_callback.new(username=username))
            keyboard.add(subscribe_button)
    else:
        keyboard.add(instagram_link)
    return keyboard


def media_keyboard(link: str):
    keyboard = InlineKeyboardMarkup()
    media_button = InlineKeyboardButton(text='📎', url=link)
    keyboard.add(media_button)
    return keyboard


def channel_keyboard(link: str):
    keyboard = InlineKeyboardMarkup()
    channel_button = InlineKeyboardButton(text='📎 Подписывайся', url=link)
    keyboard.add(channel_button)
    return keyboard

def subscribe_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton(text='3', callback_data=mutable_subscribe_callback.new(count=3)),
        InlineKeyboardButton(text='5', callback_data=mutable_subscribe_callback.new(count=5)),
        InlineKeyboardButton(text='10', callback_data=mutable_subscribe_callback.new(count=10)),
    )
    return keyboard
