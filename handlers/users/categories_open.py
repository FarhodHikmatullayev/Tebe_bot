from data.config import ADMINS
from keyboards.default.menu import back_menu_keyboard
from keyboards.inline.categories import categories_callback_data
from keyboards.inline.posts import add_or_see_posts_keyboard, create_or_not_or_back
from loader import dp, db
from aiogram.types import CallbackQuery, Message


# for employer
@dp.callback_query_handler(categories_callback_data.filter(), user_id=ADMINS)
async def open_categories(call: CallbackQuery, callback_data: dict):
    for_who = callback_data.get('for_who')
    category_id = int(callback_data.get('id'))

    if for_who == 'employee':

        posts = await db.select_posts(category_id=category_id)
        if posts:
            text = "Xodimlarning murojaatlari ro'yxati"
        else:
            text = "Hali murojaatlar mavjud emas"
        await call.message.edit_text(text=text)

        tr = 0

        for post in posts:
            tr += 1
            text = f"{tr}.\n"

            user_id = post['user_id']
            users = await db.select_users(id=user_id)
            full_name = users[0]['full_name']
            username = users[0]['username']
            phone = users[0]['phone']

            text += "Murojaat/Taklif egasi ma'lumotlari: \n"
            text += f"   username: {username} \n"
            text += f"   full_name: {full_name} \n"
            text += f"   telefon raqam: {phone} \n"

            message = post['text']
            photo_id = post['image']
            video_id = post['video']
            if message:
                text += f"Post matni: {message}\n"
            if photo_id:
                await call.message.answer_photo(photo=photo_id, caption=text)
            if video_id:
                await call.message.answer_video(video=video_id, caption=text)

        await call.message.answer(text="Asosiy menyuga qaytish uchun quyidagi tugmani bosing",
                                  reply_markup=back_menu_keyboard)

    elif for_who == "employer":
        markup = await add_or_see_posts_keyboard(category_id=category_id, for_who=for_who)
        text = "Yangi post qo'yasizmi yoki postlar ro'yxatini ko'rasizmi?"
        await call.message.edit_text(text=text, reply_markup=markup)


# for employee
@dp.callback_query_handler(categories_callback_data.filter())
async def open_categories(call: CallbackQuery, callback_data: dict):
    for_who = callback_data.get('for_who')
    category_id = int(callback_data.get('id'))

    if for_who == 'employer':

        posts = await db.select_posts(category_id=category_id)
        if posts:
            text = "Postlar ro'yxati"
        else:
            text = "Hali postlar mavjud emas"
        await call.message.edit_text(text=text)
        tr = 0

        for post in posts:
            tr += 1

            text = f"{tr}.\n"

            user_id = post['user_id']
            users = await db.select_users(id=user_id)
            full_name = users[0]['full_name']
            username = users[0]['username']
            phone = users[0]['phone']
            message = post['text']
            photo_id = post['image']
            video_id = post['video']
            text += "Post egasi ma'lumotlari: \n"
            text += f"   username: {username} \n"
            text += f"   full_name: {full_name} \n"
            text += f"   telefon raqam: {phone} \n"
            if message:
                text += f"Post matni: {message}\n"
            if photo_id:
                await call.message.answer_photo(photo=photo_id, caption=text)
            if video_id:
                await call.message.answer_video(video=video_id, caption=text)

        await call.message.answer(text="Asosiy menyuga qaytish uchun quyidagi tugmani bosing",
                                  reply_markup=back_menu_keyboard)
        if tr == 0:
            text = "Hali post mavjud emas"
            await call.message.answer(text=text, reply_markup=back_menu_keyboard)

    elif for_who == "employee":
        markup = await create_or_not_or_back(category_id=category_id, for_who=for_who)
        text = "Adminga taklif yoki muammo yuborasizmi?"
        await call.message.edit_text(text=text, reply_markup=markup)
