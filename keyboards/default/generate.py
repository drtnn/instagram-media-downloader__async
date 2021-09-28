from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

default_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🚨 Помощь')
        ]
    ],
    resize_keyboard=True
)
