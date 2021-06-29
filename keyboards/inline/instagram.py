from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .callback_datas import stories_callback, posts_callback


def user_keyboard(username: str):
    keyboard = InlineKeyboardMarkup(row_width=2)
    stories_button = InlineKeyboardButton(text='📹 Истории', callback_data=stories_callback.new(username=username))
    posts_button = InlineKeyboardButton(text='📽 Посты', callback_data=posts_callback.new(username=username))
    instagram_link = InlineKeyboardButton(text='📸 Instagram', url=f'https://www.instagram.com/{username}')
    keyboard.add(stories_button, posts_button, instagram_link)
    return keyboard
