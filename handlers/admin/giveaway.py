from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from keyboards.inline.generate import giveaway_keyboard
from loader import dp, bot
from states.admin import GiveawayState
from utils.db_api.database import Giveaway


@dp.message_handler(is_admin=True, commands=['giveaway'])
async def bot_giveaway(message: Message):
    await message.answer('🤖 Присылай сообщение для розыгрыша')
    await GiveawayState.text.set()


@dp.message_handler(is_admin=True, state=GiveawayState.text)
async def bot_giveaway_text(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    await state.reset_state()
    giveaway = await Giveaway.add()
    await bot.send_message(chat_id=-1001558820128, text=message.text,
                           reply_markup=giveaway_keyboard(giveaway_id=giveaway.id))
