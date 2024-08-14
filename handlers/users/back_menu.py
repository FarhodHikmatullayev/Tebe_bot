from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.categories import categories_keyboard
from loader import dp


@dp.message_handler(text='◀ Bosh Menyu', state='*')
async def back_to_menu(message: types.Message, state: FSMContext):
    markup = await categories_keyboard(user_id=message.from_user.id)
    text = "Quyidagi bo'limlardan birini tanlang"
    await message.answer(text, reply_markup=markup)
    await state.finish()
