from aiogram import types

from keyboards.inline.categories import categories_keyboard
from loader import dp, db


@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    categories = await db.select_all_categories()
    txt = ""
    tr = 0
    for category in categories:
        tr += 1
        txt += f"{tr}. {category['name']}\n"
    text = "Bunday buyruq mavjud emas! \n" \
           "Quyidagi bo'limlardan birini tanlang"
    await message.answer(text)
    markup = await categories_keyboard(user_id=message.from_user.id)
    if not txt:
        await message.answer(text="Hali ma'lumotlar ba'zasida hechqanday ma'lumotlar mavjud emas!")
    else:
        await message.answer(text=txt, reply_markup=markup)
