from aiogram.types import InlineQuery
from loader import dp
from utils.instagram.instagram_query_result import inline_start


@dp.inline_handler(text='', state='*')
async def info_inline(query: InlineQuery):
    await query.answer(results=inline_start(), cache_time=1)
