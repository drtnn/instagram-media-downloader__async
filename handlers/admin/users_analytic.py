from aiofiles import os, open
from aiogram.types import Message
from loader import dp
from utils.analytics.users import generate_chart


@dp.message_handler(is_admin=True, commands=['users_analytic'], state='*')
async def bot_users_analytic(message: Message):
    chart = await generate_chart(duration=7, filename=f'users_analytic_{message.chat.id}.png')
    await message.answer_photo(photo=await (await open(chart, mode='rb')).read())
    await os.remove(chart)
