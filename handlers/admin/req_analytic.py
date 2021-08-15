from aiofiles import os, open
from aiogram.types import Message
from loader import dp
from utils.analytics.requests import generate_chart


@dp.message_handler(is_admin=True, commands=['req_analytic'], state='*')
async def bot_req_analytic(message: Message):
    chart = await generate_chart(duration=7, filename=f'req_analytic_{message.chat.id}.png')
    await message.answer_photo(photo=await (await open(chart, mode='rb')).read())
    await os.remove(chart)
