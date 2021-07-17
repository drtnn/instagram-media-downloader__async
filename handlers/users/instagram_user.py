from aiogram.types import Message, CallbackQuery, InlineQuery
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageToEditNotFound
from loader import dp, bot, upload_client
from keyboards.inline.callback_datas import stories_callback
from keyboards.inline.instagram import user_keyboard
from states.inline import InlineContent
from utils.instagram import InstagramUser


@dp.message_handler(instagram_user=True, state='*')
async def instagram_user_handler(message: Message):
    user = InstagramUser(message.text.lower())
    await user.start()
    user_message: Message = await user.send_to(bot=bot, chat_id=message.chat.id)
    if user_message:
        state = dp.current_state(user=message.from_user.id)
        data = await state.get_data()
        if 'chat_id' in data and 'message_id' in data:
            try:
                await bot.edit_message_reply_markup(chat_id=data['chat_id'], message_id=data['message_id'], reply_markup=user_keyboard(user.username, user.is_private, False))
            except MessageToEditNotFound:
                pass
        await state.update_data(username=message.text.lower(), chat_id=user_message.chat.id, message_id=user_message.message_id)
        await InlineContent.post.set()


@dp.callback_query_handler(stories_callback.filter(), state='*')
async def instagram_stories_callback_query_handler(call: CallbackQuery, callback_data: dict):
    user = InstagramUser(callback_data['username'])
    await user.start()
    await user.send_stories_to(bot=bot, upload_client=upload_client, chat_id=call.from_user.id, call=call)


@dp.inline_handler(text='', state=InlineContent.post)
async def instagram_user_inline_posts(query: InlineQuery, state: FSMContext):
    data = await state.get_data()
    user = InstagramUser(data['username'])
    await user.start()
    await user.inline_posts_to(query=query, cache_time=10)


@dp.inline_handler(instagram_inline_user=True, state='*')
async def instagram_user_inline_handler(query: InlineQuery):
    user = InstagramUser(query.query.strip())
    await user.start()
    await user.inline_stories_to(query=query)
