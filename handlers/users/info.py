from aiogram.types import InlineQuery
from loader import dp
from utils.instagram.instagram_query_result import inline_start, not_inline_start


@dp.inline_handler(is_subscriber=True, text='', state='*')
async def info_inline(query: InlineQuery):
    await query.answer(results=inline_start(), cache_time=1)


@dp.inline_handler(state='*')
async def not_info_inline(query: InlineQuery):
    await query.answer(results=not_inline_start(), cache_time=1)
