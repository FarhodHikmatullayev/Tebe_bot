from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.categories import categories_keyboard
from loader import dp, db


@dp.message_handler(text='◀ Bosh Menyu', state='*')
async def back_to_menu(message: types.Message, state: FSMContext):
    categories = await db.select_all_categories()
    txt = ""
    tr = 0
    for category in categories:
        tr += 1
        txt += f"{tr}. {category['name']}\n"
    markup = await categories_keyboard(user_id=message.from_user.id)
    text = "Quyidagi bo'limlardan birini tanlang"
    await message.answer(text)
    await message.answer(text=txt, reply_markup=markup)
    await state.finish()
