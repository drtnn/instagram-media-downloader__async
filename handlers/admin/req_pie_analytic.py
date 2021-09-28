from aiofiles import os, open
from aiogram.types import Message
from loader import dp
from utils.analytics.requests import generate_pie_chart


@dp.message_handler(is_admin=True, commands=['req_pie_analytic'], state='*')
async def bot_req_pie_analytic(message: Message):
    chart = await generate_pie_chart(duration=7, filename=f'req_pie_analytic_{message.chat.id}.png')
    await message.answer_photo(photo=await (await open(chart, mode='rb')).read())
    await os.remove(chart)
