from aiogram.dispatcher.filters.state import StatesGroup, State


class InlineContent(StatesGroup):
    username = State()
    is_private = State()
    chat_id = State()
    message_id = State()
    post = State()
