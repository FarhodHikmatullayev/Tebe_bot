from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, ContentType
from asyncpg import types

from data.config import ADMINS
from keyboards.default.menu import back_menu_keyboard
from loader import dp
from states.get_photo import Photo
from states.get_video import Video
from utils.photograph import photo_link


@dp.message_handler(Command('get_photo_id'), user_id=ADMINS, state='*')
async def start_getting_photo_url(message: Message, state: FSMContext):
    await state.finish()
    text = "Rasm jo'nating"
    await message.answer(text=text, reply_markup=back_menu_keyboard)
    await Photo.photo.set()


@dp.message_handler(Command('get_photo_id'), state='*')
async def start_getting_photo_url(message: Message, state: FSMContext):
    await state.finish()
    text = "Bu funksiya faqat ADMIN uchun, sizda ruhsat yo'q"
    await message.answer(text=text, reply_markup=back_menu_keyboard)


@dp.message_handler(content_types=ContentType.PHOTO, state=Photo.photo)
async def get_photo(message: Message, state: FSMContext):
    photo = message.photo[-1].file_id
    # link = await photo_link(photo)
    await message.answer(text=photo)
    await state.finish()


@dp.message_handler(content_types=ContentType.ANY, state=Photo.photo)
async def get_photo(message: Message, state: FSMContext):
    text = "Siz rasm jo'natishingiz kerak\n" \
           "Iltimos qayta urunib ko'ring"
    await message.answer(text=text, reply_markup=back_menu_keyboard)
    await state.set_state(Photo.photo)

@dp.message_handler(content_types=ContentType.ANY, state=Video.video)
async def get_video(message: Message, state: FSMContext):
    text = "Siz video jo'natishingiz kerak\n" \
           "Iltimos qayta urunib ko'ring"
    await message.answer(text=text, reply_markup=back_menu_keyboard)
    await state.set_state(Video.video)
