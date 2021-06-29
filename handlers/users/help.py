from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    await message.answer('💭 Скачиваю весь контент из <pre>Instagram</pre>.\n\n🔗 Просто отправь ссылку на пост, историю или никнейм.\n\n\t🎞: <code>instagram.com/p/*****/</code>\n\t📹: <code>instagram.com/stories/drtagram/*****/</code>\n\t👤: <code>drtagram</code>\n\n💬 Чтобы отправить публикацию другу в диалог, воспользуйся <pre>inline</pre>-режимом бота.\n\n\t🎞: <code>@InstagramMediaDownloadBot instagram.com/p/*****/</code>\n\t📹: <code>@InstagramMediaDownloadBot instagram.com/stories/drtagram/*****/</code>\n\t👤: <code>@InstagramMediaDownloadBot drtagram</code>')
