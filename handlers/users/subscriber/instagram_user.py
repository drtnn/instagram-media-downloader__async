from aiogram.types import Message, CallbackQuery, InlineQuery
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageToEditNotFound
from loader import dp, bot, upload_client
from keyboards.inline.callback_datas import stories_callback
from keyboards.inline.generate import user_keyboard
from states.inline import InlineContent
from utils.db_api.database import Requests
from utils.instagram import InstagramUser


@dp.message_handler(is_subscriber=True, instagram_user=True, state='*')
async def instagram_user_handler(message: Message):
    user = InstagramUser(message.text.lower())
    await user.start()
    user_message: Message = await user.send_to(bot=bot, chat_id=message.chat.id)
    if user_message:
        state = dp.current_state(user=message.from_user.id)
        data = await state.get_data()
        if 'chat_id' in data and 'message_id' in data:
            try:
                await bot.edit_message_reply_markup(chat_id=data['chat_id'], message_id=data['message_id'],
                                                    reply_markup=user_keyboard(username=data['username'],
                                                                               is_private=data['is_private'],
                                                                               posts_button=False))
            except MessageToEditNotFound:
                pass
        await state.update_data(username=user.username, is_private=user.is_private, chat_id=user_message.chat.id,
                                message_id=user_message.message_id)
        await InlineContent.post.set()
    await Requests.add(user_id=message.from_user.id, content_type='u')


@dp.callback_query_handler(stories_callback.filter(), is_subscriber=True, state='*')
async def instagram_stories_callback_query_handler(call: CallbackQuery, callback_data: dict):
    user = InstagramUser(callback_data['username'])
    await user.start()
    await user.send_stories_to(bot=bot, upload_client=upload_client, chat_id=call.from_user.id, call=call)
    await Requests.add(user_id=call.from_user.id, content_type='s')


@dp.inline_handler(is_subscriber=True, text='', state=InlineContent.post)
async def instagram_user_inline_posts(query: InlineQuery, state: FSMContext):
    data = await state.get_data()
    user = InstagramUser(data['username'])
    await user.start()
    await user.inline_posts_to(query=query, cache_time=10)
    await Requests.add(user_id=query.from_user.id, content_type='p')


@dp.inline_handler(is_subscriber=True, instagram_inline_user=True, state='*')
async def instagram_user_inline_handler(query: InlineQuery):
    user = InstagramUser(query.query.strip())
    await user.start()
    await user.inline_stories_to(query=query)
    await Requests.add(user_id=query.from_user.id, content_type='u')
