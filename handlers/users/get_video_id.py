from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, ContentType
from asyncpg import types

from data.config import ADMINS
from keyboards.default.menu import back_menu_keyboard
from loader import dp
from states.get_photo import Photo
from states.get_video import Video
from utils.photograph import video_link


@dp.message_handler(Command('get_video_id'), user_id=ADMINS, state='*')
async def start_getting_video_url(message: Message, state: FSMContext):
    await state.finish()
    text = "Video jo'nating"
    await message.answer(text=text, reply_markup=back_menu_keyboard)
    await Video.video.set()


@dp.message_handler(Command('get_video_id'), state='*')
async def start_getting_video_url(message: Message, state: FSMContext):
    await state.finish()
    text = "Bu funksiya faqat ADMIN uchun, sizda ruhsat yo'q"
    await message.answer(text=text, reply_markup=back_menu_keyboard)


@dp.message_handler(content_types=ContentType.VIDEO, state=Video.video)
async def get_video(message: Message, state: FSMContext):
    video = message.video.file_id
    # link = await video_link(video)
    await message.answer(text=video)
    await state.finish()



