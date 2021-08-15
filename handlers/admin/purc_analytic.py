from aiofiles import os, open
from aiogram.types import Message
from loader import dp
from utils.analytics.purchases import generate_chart


@dp.message_handler(is_admin=True, commands=['purc_analytic'], state='*')
async def bot_purc_analytic(message: Message):
    chart = await generate_chart(duration=7, filename=f'subs_analytic_{message.chat.id}.png')
    await message.answer_photo(photo=await (await open(chart, mode='rb')).read())
    await os.remove(chart)
