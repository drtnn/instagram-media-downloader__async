from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def channel_keyboard(link: str):
    keyboard = InlineKeyboardMarkup()
    channel_button = InlineKeyboardButton(text='📎 Подписывайся', url=link)
    keyboard.add(channel_button)
    return keyboard
