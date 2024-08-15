from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from data.config import ADMINS
from loader import db

categories_callback_data = CallbackData('category', 'id', 'for_who')


async def categories_keyboard(user_id):
    markup = InlineKeyboardMarkup(row_width=5)
    admins = list(map(int, ADMINS))
    categories = await db.select_all_categories()

    # if user_id in admins:
    # else:
    #     categories = await db.select_categories(for_who='employee')
    buttons = []
    tr = 0
    for category in categories:
        tr += 1
        text_button = tr
        callback_data = categories_callback_data.new(id=category['id'], for_who=category['for_who'])
        buttons.append(InlineKeyboardButton(text=text_button, callback_data=callback_data))
        if len(buttons) == 5:
            markup.add(*buttons)
            buttons = []
    if buttons:
        markup.add(*buttons)

    return markup
