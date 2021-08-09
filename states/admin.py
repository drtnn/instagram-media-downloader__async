from aiogram.dispatcher.filters.state import StatesGroup, State


class MailingState(StatesGroup):
    text = State()


class GiveawayState(StatesGroup):
    text = State()
