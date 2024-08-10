from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from data.config import ADMINS
from loader import db

categories_callback_data = CallbackData('category', 'name', 'for_who')


async def categories_keyboard(user_id):
    markup = InlineKeyboardMarkup(row_width=1)
    admins = list(map(int, ADMINS))

    if user_id in admins:
        categories = await db.select_all_categories()
    else:
        categories = await db.select_categories(for_who='employee')
    for category in categories:
        text_button = f"{category['name']}".capitalize()
        callback_data = categories_callback_data.new(name=category['name'], for_who=category['for_who'])
        markup.insert(
            InlineKeyboardButton(
                text=text_button,
                callback_data=callback_data
            )
        )

    return markup
