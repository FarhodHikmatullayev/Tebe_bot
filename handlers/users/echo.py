from aiogram import types

from keyboards.inline.categories import categories_keyboard
from loader import dp


@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    text = "Bunday buyruq mavjud emas! \n" \
           "Quyidagi bo'limlardan birini tanlang"
    markup = await categories_keyboard(user_id=message.from_user.id)

    await message.answer(text, reply_markup=markup)
