from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from loader import dp


@dp.message_handler(is_admin=True, commands=['cancel'], state='*')
async def bot_admin_cancel(message: Message, state: FSMContext):
    await state.reset_state()
