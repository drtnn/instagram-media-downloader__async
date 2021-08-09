from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

default_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='💲 Подписка'),
            KeyboardButton(text='👥 Реферальная программа'),
        ],
        [
            KeyboardButton(text='🚨 Помощь')
        ]
    ],
    resize_keyboard=True
)
