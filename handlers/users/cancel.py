from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from loader import dp


@dp.message_handler(commands=['cancel'], state='*')
async def bot_admin_cancel(_: Message, state: FSMContext):
    await state.reset_state()
