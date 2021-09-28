from aiofiles import os, open
from aiogram.types import Message, InputFile, MediaGroup
from loader import dp
from utils.analytics import users, purchases, requests


@dp.message_handler(is_admin=True, commands=['analytic'], state='*')
async def bot_analytic(message: Message):
    charts = [
        await users.generate_chart(duration=7, filename=f'users_analytic_{message.chat.id}.png'),
        await purchases.generate_chart(duration=7, filename=f'purc_analytic_{message.chat.id}.png'),
        await requests.generate_chart(duration=7, filename=f'req_analytic_{message.chat.id}.png'),
        await requests.generate_pie_chart(duration=7, filename=f'req_pie_analytic_{message.chat.id}.png'),
    ]

    media_group = MediaGroup()
    for chart in charts:
        media_group.attach_photo(InputFile(chart))

    await message.answer_media_group(media_group)

    for chart in charts:
        await os.remove(chart)
