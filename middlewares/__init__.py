from aiogram import Dispatcher

from loader import dp
from .throttling import ThrottlingMiddleware
from .logger import LoggingMiddleware, LOGFILE


if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(LoggingMiddleware(logger=LOGFILE))
