from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from data.config import ADMINS
from loader import db

add_or_select_callback_data = CallbackData('post', 'category_id', 'for_who', 'create_or_read')
vide_or_image_or_no = CallbackData('create_post', 'image_video_nothing')


async def add_or_see_posts_keyboard(category_id, for_who):
    print('category_id', category_id)
    print('for_who', for_who)
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Post yaratish",
                    callback_data=add_or_select_callback_data.new(category_id=category_id, for_who=for_who,
                                                                  create_or_read='create')
                ),
                InlineKeyboardButton(
                    text="Postlarni ko'rish",
                    callback_data=add_or_select_callback_data.new(category_id=category_id, for_who=for_who,
                                                                  create_or_read='read')
                )
            ],
            [
                InlineKeyboardButton(
                    text='Orqaga',
                    callback_data=add_or_select_callback_data.new(category_id=category_id, for_who=for_who,
                                                                  create_or_read='back')
                )
            ]
        ]
    )
    return markup


async def create_or_not_or_back(category_id, for_who):
    print('category_id', category_id)
    print('for_who', for_who)
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Murojaat yo'llash",
                    callback_data=add_or_select_callback_data.new(category_id=category_id, for_who=for_who,
                                                                  create_or_read='yes')
                )
            ],
            [
                InlineKeyboardButton(
                    text="Mening Murojaat/Takliflarim",
                    callback_data=add_or_select_callback_data.new(category_id=category_id, for_who=for_who,
                                                                  create_or_read='my_posts')
                )
            ],
            [
                InlineKeyboardButton(
                    text='Orqaga',
                    callback_data=add_or_select_callback_data.new(category_id=category_id, for_who=for_who,
                                                                  create_or_read='back')
                )
            ]
        ]
    )
    return markup


async def video_image_or_nothing():
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Rasm",
                    callback_data=vide_or_image_or_no.new(
                        image_video_nothing='photo'
                    )
                ),
                InlineKeyboardButton(
                    text="Video",
                    callback_data=vide_or_image_or_no.new(
                        image_video_nothing='video'
                    )
                )
            ],
            [
                InlineKeyboardButton(
                    text='Yo\'q shartmas',
                    callback_data=vide_or_image_or_no.new(
                        image_video_nothing='nothing'
                    )
                )
            ]
        ]
    )
    return markup
