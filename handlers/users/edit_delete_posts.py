from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, ContentType

from data.config import ADMINS
from keyboards.default.menu import back_menu_keyboard
from keyboards.inline.confirmation import confirm_keyboard
from keyboards.inline.edit_posts import get_choose_button, text_or_video_or_image, edit_or_delete_inline_keyboard, \
    edit_or_delete_callback_data
from loader import dp, db, bot
from states.posts_state import PostEditDelete
from utils.photograph import photo_link, video_link


@dp.callback_query_handler(text='ok')
async def confirm_edit_delete(call: CallbackQuery):
    if str(call.from_user.id) in ADMINS:
        text = "O'zgartirmoqchi yoki o'chirmoqchi bo'lgan Postingizning ID raqamini kiriting"
    else:
        text = "O'zgartirmoqchi yoki o'chirmoqchi bo'lgan Murojaat/Taklifingizning ID raqamini kiriting"
    await PostEditDelete.id.set()
    await call.message.answer(text=text, reply_markup=back_menu_keyboard)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


@dp.callback_query_handler(text='cancel')
async def cancel_edit_delete(call: CallbackQuery):
    user_telegram_id = call.from_user.id
    users = await db.select_users(telegram_id=user_telegram_id)
    user_id = users[0]['id']
    if user_id in ADMINS:
        text = "Siz Postingizni o'zgartirishni rad etdingiz"
    else:
        text = "Siz Murojaat/Taklifingizni o'zgartirishni rad etdingiz"
    await call.message.answer(text=text, reply_markup=back_menu_keyboard)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


@dp.message_handler(state=PostEditDelete.id)
async def get_post_id(message: Message, state: FSMContext):
    user_telegram_id = message.from_user.id
    users = await db.select_users(telegram_id=user_telegram_id)
    user_id = users[0]['id']
    post_id = message.text

    try:
        post_id = int(post_id)

        posts = await db.select_posts(id=post_id, user_id=user_id)
        if posts:
            post = posts[0]

            if str(message.from_user.id) in ADMINS:
                text = "Bu postni taxrirlaysizmi yoki o'chirasizmi?"
            else:
                text = "Bu Murojaat/Taklifni taxrirlaysizmi yoki o'chirasizmi?"
            markup = await edit_or_delete_inline_keyboard(post_id=post_id)
            await message.answer(text=text, reply_markup=markup)

            await state.update_data(
                {
                    'post_id': post_id,
                    'image': post['image'],
                    'video': post['video'],
                    'text': post['text']
                }
            )


        else:
            text = "Bunday ID raqamli post mavjud emas\n" \
                   "Iltimos tog'ri ID raqam kiriting"
            await PostEditDelete.id.set()
            await message.answer(text=text, reply_markup=back_menu_keyboard)

    except:
        text = "ID raqam bo'ladi va u tepadagi postlaringizda yozilgan\n" \
               "Iltimos tog'ri ID raqam kiriting"
        await PostEditDelete.id.set()
        await message.answer(text=text, reply_markup=back_menu_keyboard)


@dp.callback_query_handler(edit_or_delete_callback_data.filter(), state=PostEditDelete.id)
async def edit_or_delete(call: CallbackQuery, state: FSMContext, callback_data: dict):
    edit_or_delete = callback_data.get('edit_or_delete')
    post_id = int(callback_data.get('post_id'))

    if edit_or_delete == 'delete':

        await db.delete_post(id=post_id)

        if str(call.from_user.id) in ADMINS:
            text = "Sizning Postingiz muvaffaqiyatli o'chirildi"

        else:
            text = "Sizning Taklif/Murojaatingiz muvaffaqiyatli o'chirildi"
        await call.message.answer(text=text, reply_markup=back_menu_keyboard)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

        await state.finish()

    elif edit_or_delete == 'edit':
        user_telegram_id = call.from_user.id
        users = await db.select_users(telegram_id=user_telegram_id)
        user_id = users[0]['id']
        posts = await db.select_posts(id=post_id, user_id=user_id)

        post = posts[0]
        post_image = post['image']
        post_video = post['video']

        if post_image:
            markup = await get_choose_button(post_id=post_id, video_image='image')
            text = "Rasmni o'zgartirasizmi yoki text?"
            await call.message.edit_text(text=text, reply_markup=markup)
        elif post_video:
            markup = await get_choose_button(post_id=post_id, video_image='video')
            text = "Videoni o'zgartirasizmi yoki text?"
            await call.message.edit_text(text=text, reply_markup=markup)
        else:
            text = "Yangi text kiriting"
            await call.message.answer(text=text, reply_markup=back_menu_keyboard)
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            await PostEditDelete.text.set()


@dp.callback_query_handler(text_or_video_or_image.filter(), state=PostEditDelete.id)
async def edit_kwargs(call: CallbackQuery, state: FSMContext, callback_data: dict):
    post_id = callback_data.get('post_id')
    text_video_image = callback_data.get('text_video_image')
    if text_video_image == 'text':
        text = "Yangi text kiriting"
        await PostEditDelete.text.set()
        await call.message.edit_text(text=text)
    elif text_video_image == 'image':
        text = "Yangi rasm kiriting"
        await state.set_state(PostEditDelete.image.state)
        await call.message.edit_text(text=text)
    elif text_video_image == 'video':
        text = "Yangi video kiriting"
        await state.set_state(PostEditDelete.video.state)
        await call.message.edit_text(text=text)
    elif text_video_image == 'both':
        await state.update_data(
            {
                'text': 'both'
            }
        )
        text = "Yangi text kiriting"
        await PostEditDelete.text.set()
        await call.message.edit_text(text=text)


@dp.message_handler(state=PostEditDelete.text)
async def edit_text(message: Message, state: FSMContext):
    data = await state.get_data()
    state_text = data.get('text')
    text = message.text
    await state.update_data(
        {
            'text': text
        }
    )
    if state_text == 'both':
        data = await state.get_data()
        image = data.get('image')
        video = data.get('video')
        if image:
            text = "Yangi rasm kiriting"
            await state.set_state(PostEditDelete.image.state)
            await message.answer(text=text)
        elif video:
            text = "Yangi video kiriting"
            await state.set_state(PostEditDelete.video.state)
            await message.answer(text=text)
    else:
        data = await state.get_data()
        id = data.get('post_id')

        posts = await db.select_posts(id=id)
        post = posts[0]

        text = data.get('text', post['text'])
        image = data.get('image', post['image'])
        video = data.get('video', post['video'])

        print('video', video)
        print('image', image)

        txt = f"Text: {text}\n"
        if image:
            txt += f"Rasm: {image}\n"
        elif video:
            txt += f"Video: {video}\n"

        if str(message.from_user.id) in ADMINS:
            text = "Sizning postingiz o'zgartirishdan so'ng tepadagidek bo'ladi\n"
        else:
            text = "Sizning Murojaat/Taklifingiz o'zgartishdan so'ng tepadagidek bo'ladi\n"
        await message.answer(text=txt)
        await message.answer(text=text + "O'zarishlar saqlansinmi?", reply_markup=confirm_keyboard)
        await state.set_state(PostEditDelete.edit.state)


@dp.message_handler(state=PostEditDelete.image, content_types=ContentType.PHOTO)
async def edit_image(message: Message, state: FSMContext):
    photo = message.photo[-1]
    link = await photo_link(photo)
    await state.update_data(
        {
            'image': link
        }
    )

    data = await state.get_data()
    id = data.get('post_id')

    posts = await db.select_posts(id=id)
    post = posts[0]

    text = data.get('text', post['text'])
    image = data.get('image', post['image'])
    video = data.get('video', post['video'])

    print('image', image)
    print('video', video)

    txt = f"Text: {text}\n"
    if image:
        txt += f"Rasm: {image}\n"
    elif video:
        txt += f"Video: {video}\n"
    if str(message.from_user.id) in ADMINS:
        text = "Sizning postingiz o'zgartirishdan so'ng tepadagidek bo'ladi\n"
    else:
        text = "Sizning Murojaat/Taklifingiz o'zgartishdan so'ng tepadagidek bo'ladi\n"
    await message.answer(text=txt)
    await message.answer(text=text + "O'zarishlar saqlansinmi?", reply_markup=confirm_keyboard)
    await state.set_state(PostEditDelete.edit.state)


@dp.message_handler(state=PostEditDelete.image, content_types=ContentType.ANY)
async def edit_image(message: Message, state: FSMContext):
    text = "Siz rasm kiritishingiz kerak\n" \
           "Iltimos qaytadan rasm yuboring"
    await message.answer(text=text, reply_markup=back_menu_keyboard)


@dp.message_handler(state=PostEditDelete.video, content_types=ContentType.VIDEO)
async def edit_video(message: Message, state: FSMContext):
    video = message.video
    link = await video_link(video=video)
    await state.update_data(
        {
            'video': link
        }
    )

    data = await state.get_data()
    id = data.get('post_id')

    posts = await db.select_posts(id=id)
    post = posts[0]

    text = data.get('text', post['text'])
    image = data.get('image', post['image'])
    video = data.get('video', post['video'])

    print('image', image)
    print('video', video)

    txt = f"Text: {text}\n"
    if image:
        txt += f"Rasm: {image}\n"
    elif video:
        txt += f"Video: {video}\n"
    if str(message.from_user.id) in ADMINS:
        text = "Sizning postingiz o'zgartirishdan so'ng tepadagidek bo'ladi\n"
    else:
        text = "Sizning Murojaat/Taklifingiz o'zgartishdan so'ng tepadagidek bo'ladi\n"
    await message.answer(text=txt)
    await message.answer(text=text + "O'zarishlar saqlansinmi?", reply_markup=confirm_keyboard)
    await state.set_state(PostEditDelete.edit.state)


@dp.message_handler(state=PostEditDelete.video, content_types=ContentType.ANY)
async def edit_video(message: Message, state: FSMContext):
    text = "Siz video kiritishingiz kerak\n" \
           "Iltimos qayta video jo'nating"
    await message.answer(text=text, reply_markup=back_menu_keyboard)


@dp.callback_query_handler(text='ok', state=PostEditDelete.edit)
async def confirm_edit_post(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    print('data', data)
    id = data.get('post_id')
    image = data.get('image')
    video = data.get('video')
    text = data.get('text')
    await db.update_post(
        id=id,
        text=text,
        image=image,
        video=video
    )

    if str(call.from_user.id) in ADMINS:
        text = "Siz Postni muvaffaqiyatli taxrirladingiz"
    else:
        text = "Siz Murojaat/Taklifingizni muvaffaqiyatli taxrirladingiz"
    await call.message.answer(text=text, reply_markup=back_menu_keyboard)
    await state.finish()
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


@dp.callback_query_handler(text='cancel', state=PostEditDelete.edit)
async def cancel_edit_post(call: CallbackQuery, state: FSMContext):
    text = "Siz o'zgartirishni rad etdingiz"
    await call.message.answer(text=text, reply_markup=back_menu_keyboard)
    await state.finish()
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
