from data.config import ADMINS
from keyboards.inline.categories import categories_callback_data
from keyboards.inline.posts import add_or_see_posts_keyboard, create_or_not_or_back
from loader import dp, db
from aiogram.types import CallbackQuery, Message


# for employer
@dp.callback_query_handler(categories_callback_data.filter(), user_id=ADMINS)
async def open_categories(call: CallbackQuery, callback_data: dict):
    for_who = callback_data.get('for_who')
    category_id = int(callback_data.get('id'))
    print('category_id', category_id)
    print('callback_data', callback_data)

    if for_who == 'employee':
        text = "Xodimlarning murojaatlari ro'yxati"
        await call.message.edit_text(text=text)
        posts = await db.select_posts(category_id=category_id)
        tr = 0
        for post in posts:
            text = ""
            message = post['text']
            photo_url = post['image']
            video_url = post['video']
            tr += 1
            if message:
                text += f"{message}\n"
            if photo_url:
                text += f"{photo_url}\n"
            if video_url:
                text += f"{video_url}"

            await call.message.answer(text=text)

    elif for_who == "employer":
        markup = await add_or_see_posts_keyboard(category_id=category_id, for_who=for_who)
        text = "Yangi post qo'yasizmi yoki postlar ro'yxatini ko'rasizmi?"
        await call.message.edit_text(text=text, reply_markup=markup)


# for employee
@dp.callback_query_handler(categories_callback_data.filter())
async def open_categories(call: CallbackQuery, callback_data: dict):
    for_who = callback_data.get('for_who')
    category_id = int(callback_data.get('id'))
    print('category_id', category_id)
    print('callback_data', callback_data)

    if for_who == 'employer':
        text = "Postlar ro'yxati"
        await call.message.edit_text(text=text)
        posts = await db.select_posts(category_id=category_id)
        tr = 0
        for post in posts:
            text = ""
            message = post['text']
            photo_url = post['image']
            video_url = post['video']
            tr += 1
            if message:
                text += f"{message}\n"
            if photo_url:
                text += f"{photo_url}\n"
            if video_url:
                text += f"{video_url}"

            await call.message.answer(text=text)

    elif for_who == "employee":
        markup = await create_or_not_or_back(category_id=category_id, for_who=for_who)
        text = "Adminga taklif yoki muammo yuborasizmi?"
        await call.message.edit_text(text=text, reply_markup=markup)
