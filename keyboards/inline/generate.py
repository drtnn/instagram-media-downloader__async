from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .callback_datas import stories_callback, subscribe_callback
from data.config import BOT_NAME
from utils.payment.invoice_data import duration_to_info


def user_keyboard(username: str, is_private: bool, posts_button: bool = True):
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
    channel_button = InlineKeyboardButton(text='📎 Подписаться', url=link)
    keyboard.add(channel_button)
    return keyboard


def subscribe_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.row(
        InlineKeyboardButton(text=f'💳 2 недели – {duration_to_info[14]["price"]}₽',
                             callback_data=subscribe_callback.new(duration=14)),
        InlineKeyboardButton(text=f'💸 1 месяц – {duration_to_info[30]["price"]}₽',
                             callback_data=subscribe_callback.new(duration=30))
    )
    keyboard.add(
        InlineKeyboardButton(text=f'💰 3 месяца – {duration_to_info[90]["price"]}₽',
                             callback_data=subscribe_callback.new(duration=90))
    )
    return keyboard


def payment_keyboard(url: str, price: int):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(text=f'💵 Оплатить {price}₽',
                             url=url)
    )
    return keyboard


def giveaway_keyboard(giveaway_id: str):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(text='✔️ Участвовать',
                             url=f't.me/{BOT_NAME}?start=giveaway_{giveaway_id}')
    )
    return keyboard
