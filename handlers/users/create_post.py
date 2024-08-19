from aiogram.dispatcher import FSMContext
import datetime
from data.config import ADMINS
from keyboards.default.menu import back_menu_keyboard
from keyboards.inline.categories import categories_callback_data, categories_keyboard
from keyboards.inline.confirmation import confirm_keyboard
from keyboards.inline.edit_posts import text_or_video_or_image
from keyboards.inline.posts import add_or_see_posts_keyboard, add_or_select_callback_data, video_image_or_nothing, \
    vide_or_image_or_no
from loader import dp, db, bot
from aiogram.types import CallbackQuery, Message, ContentType

from states.posts_state import Post
from utils.photograph import photo_link, video_link


# for employer
@dp.callback_query_handler(add_or_select_callback_data.filter(), user_id=ADMINS)
async def read_or_add_or_back_to_categories(call: CallbackQuery, callback_data: dict, state: FSMContext):
    create_or_read = callback_data.get("create_or_read")
    category_id = int(callback_data.get("category_id"))
    for_who = callback_data.get("for_who")
    if create_or_read == 'back':

        categories = await db.select_all_categories()
        txt = ""
        tr = 0
        for category in categories:
            tr += 1
            txt += f"{tr}. {category['name']}\n"

        markup = await categories_keyboard(user_id=call.from_user.id)
        await call.message.edit_text(text="Endi quyidagi bo'limlardan birini tanlang")
        await call.message.answer(text=txt, reply_markup=markup)
    elif create_or_read == 'read':

        posts = await db.select_posts(category_id=category_id)
        if posts:
            text = "Qo'yilgan postlar ro'yxati"
            await call.message.edit_text(text=text)
        else:
            text = "Hali post mavjud emas"
            await call.message.answer(text=text, reply_markup=back_menu_keyboard)
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        tr = 0
        for post in posts:
            tr += 1

            text = f"{tr}.\n"

            user_id = post['user_id']
            users = await db.select_users(id=user_id)
            full_name = users[0]['full_name']
            username = users[0]['username']
            phone = users[0]['phone']

            text += "Post egasi ma'lumotlari: \n"
            text += f"   username: {username} \n"
            text += f"   full_name: {full_name} \n"
            text += f"   telefon raqam: {phone} \n"
            message = post['text']
            photo_url = post['image']
            video_url = post['video']
            if message:
                text += f"Post matni: {message}\n"
            if photo_url:
                text += f"Post rasmi: {photo_url}\n"
            if video_url:
                text += f"Post videosi: {video_url}"

            await call.message.answer(text=text)
    elif create_or_read == 'create':
        await state.update_data(
            {
                'for_who': for_who,
                'category_id': category_id,
            }
        )
        text = "Yaratmoqchi bo'lgan postingizga izoh yozing"
        await call.message.edit_text(text=text)
        await Post.text.set()

    elif create_or_read == "my_posts":
        user = await db.select_users(telegram_id=call.from_user.id)
        my_posts = await db.select_posts(user_id=user[0]['id'])
        tr = 0
        for post in my_posts:
            tr += 1

            text = f"{tr}.\n"

            category_id = post['category_id']
            category = await db.select_categories(id=category_id)
            category_name = category[0]['name']
            message = post['text']
            photo_url = post['image']
            video_url = post['video']
            text += f"Kategoriya: {category_name}\n"
            if message:
                text += f"Text: {message}\n"
            if photo_url:
                text += f"Rasm: {photo_url}\n"
            if video_url:
                text += f"Video: {video_url}\n"
            text += f"ID: {post['id']}"
            await call.message.answer(text=text)
        if tr > 0:
            txt = "Bulardan birortasini o'chirishni yoki taxrirlashni xohlaysizmi?"
            await call.message.answer(text=txt, reply_markup=confirm_keyboard)
        else:
            txt = "Siz hali Post joylamadingiz"
            await call.message.answer(text=txt, reply_markup=back_menu_keyboard)
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


# for employee
@dp.callback_query_handler(add_or_select_callback_data.filter())
async def read_or_add_or_back_to_categories(call: CallbackQuery, callback_data: dict, state: FSMContext):
    create_or_read = callback_data.get("create_or_read")
    category_id = int(callback_data.get("category_id"))
    for_who = callback_data.get("for_who")
    if create_or_read == 'back':

        categories = await db.select_all_categories()
        txt = ""
        tr = 0
        for category in categories:
            tr += 1
            txt += f"{tr}. {category['name']}\n"

        markup = await categories_keyboard(user_id=call.from_user.id)
        await call.message.edit_text(text="Endi quyidagi bo'limlardan birini tanlang")
        await call.message.answer(text=txt, reply_markup=markup)
    elif create_or_read == 'yes':
        await state.update_data(
            {
                'for_who': for_who,
                'category_id': category_id,
            }
        )
        text = "Muammo yoki taklifni kiriting"
        await call.message.edit_text(text=text)
        await Post.text.set()
    elif create_or_read == 'my_posts':
        user = await db.select_users(telegram_id=call.from_user.id)

        my_posts = await db.select_posts(user_id=user[0]['id'])
        tr = 0

        for post in my_posts:
            tr += 1

            text = f"{tr}.\n"

            category_id = post['category_id']
            category = await db.select_categories(id=category_id)
            category_name = category[0]['name']
            message = post['text']
            photo_url = post['image']
            video_url = post['video']
            text += f"Kategoriya: {category_name}\n"
            if message:
                text += f"Text: {message}\n"
            if photo_url:
                text += f"Rasm: {photo_url}\n"
            if video_url:
                text += f"Video: {video_url}"
            text += f"ID: {post['id']}"
            await call.message.answer(text=text)
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        if tr > 0:
            txt = "Bulardan birortasini o'chirishni yoki taxrirlashni xohlaysizmi?"
            await call.message.answer(text=txt, reply_markup=confirm_keyboard)
        else:
            txt = "Siz hali Murojaat/Taklif jo'natmadingiz"
            await call.message.answer(text=txt, reply_markup=back_menu_keyboard)
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


# for employer
@dp.message_handler(state=Post.text, user_id=ADMINS)
async def add_text(message: Message, state: FSMContext):
    text = message.text
    await state.update_data(
        {
            'message': text
        }
    )
    text = "Bu Postga rasm yoki video qo'shasizmi?"
    markup = await video_image_or_nothing()
    await message.answer(text=text, reply_markup=markup)


@dp.callback_query_handler(vide_or_image_or_no.filter(), state=Post.text)
async def image_or_video_button(call: CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()
    message = data.get('message')
    image_or_video = callback_data.get('image_video_nothing')
    if image_or_video == 'photo':
        text = "Rasm yuboring"
        await call.message.edit_text(text=text)
        await Post.image.set()
    elif image_or_video == 'video':
        text = "Videoni yuboring"
        await call.message.edit_text(text=text)
        await Post.video.set()

    elif image_or_video == 'nothing':
        if str(call.message.from_user.id) in ADMINS:
            text = f"Sizning Postingiz:\n" \
                   f"{message}"
        else:
            text = f"Sizning Murojaat/Taklifingiz:\n" \
                   f"{message}"
        await call.message.edit_text(text=text)
        text = 'Uni saqlashni xohlaysizmi'
        markup = confirm_keyboard
        await call.message.answer(text=text, reply_markup=markup)


# for employee
@dp.message_handler(state=Post.text)
async def add_text(message: Message, state: FSMContext):
    text = message.text
    await state.update_data(
        {
            'message': text
        }
    )
    text = "Bu Murojaat/Taklifga rasm yoki video qo'shasizmi?"
    markup = await video_image_or_nothing()
    await message.answer(text=text, reply_markup=markup)


@dp.callback_query_handler(text='ok', state=[Post.text, Post.video, Post.image])
async def create_post_only_text(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    message = data.get('message')
    category_id = data.get('category_id')
    for_who = data.get('for_who')
    image = data.get('image', None)
    video = data.get('video', None)
    user_telegram_id = call.from_user.id
    users = await db.select_users(telegram_id=user_telegram_id)
    post = await db.create_post(
        user_id=users[0]['id'],
        category_id=category_id,
        text=message,
        image=image,
        video=video,
        created_time=datetime.datetime.now() + datetime.timedelta(hours=5)
    )

    if call.from_user.id in ADMINS:
        text = "Sizning postingiz muvaffaqiyatli saqlandi"
    else:
        text = 'Sizning Murojaat/Taklifingiz muvaffaqiyatli saqlandi'
    await call.message.answer(text=text, reply_markup=back_menu_keyboard)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


@dp.callback_query_handler(text='cancel', state=[Post.text, Post.video, Post.image])
async def cancel_post(call: CallbackQuery, state: FSMContext):
    text = "Siz saqlashni rad etdingiz"
    await call.message.edit_text(text=text, reply_markup=back_menu_keyboard)


@dp.message_handler(content_types=[ContentType.PHOTO], state=Post.image)
async def save_image_for_post(message: Message, state: FSMContext):
    photo = message.photo[-1]
    link = await photo_link(photo)
    await state.update_data(
        {
            'image': link
        }
    )
    data = await state.get_data()
    msg = data.get('message')
    text = f"{link}\n" \
           f"{msg}"

    await message.answer(text=text)

    if str(message.from_user.id) in ADMINS:
        text = "Sizning Postingiz yuqoridagidek bo'ldi,\n" \
               "Uni saqlashni xohlaysizmi?"
    else:
        text = "Sizning Taklif/Murojaatingiz yuqoridagidek bo'ldi\n" \
               "Uni saqlashni xohlaysizmi?"

    await message.answer(text=text, reply_markup=confirm_keyboard)


@dp.message_handler(content_types=ContentType.ANY, state=Post.image)
async def save_image_for_post(message: Message, state: FSMContext):
    text = "Iltimos rasm jo'nating"
    await message.answer(text=text, reply_markup=back_menu_keyboard)


@dp.message_handler(content_types=[ContentType.VIDEO], state=Post.video)
async def save_video_for_post(message: Message, state: FSMContext):
    video = message.video
    link = await video_link(video=video)
    await state.update_data(
        {
            'video': link
        }
    )
    data = await state.get_data()
    msg = data.get('message')
    text = f"{link}\n" \
           f"{msg}"

    await message.answer(text=text)

    if str(message.from_user.id) in ADMINS:
        text = "Sizning Postingiz yuqoridagidek bo'ldi,\n" \
               "Uni saqlashni xohlaysizmi?"
    else:
        text = "Sizning Taklif/Murojaatingiz yuqoridagidek bo'ldi\n" \
               "Uni saqlashni xohlaysizmi?"

    await message.answer(text=text, reply_markup=confirm_keyboard)


@dp.message_handler(content_types=ContentType.ANY, state=Post.video)
async def save_video_for_post(message: Message, state: FSMContext):
    text = "Iltimos video jo'nating"
    await message.answer(text=text, reply_markup=back_menu_keyboard)
