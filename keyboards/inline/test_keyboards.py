from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

answers_keyboard_data = CallbackData('answer', 'test_id', 'time')

test_category_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Mutaxasislar uchun",
                callback_data='specialist'
            ),
            InlineKeyboardButton(
                text="Ishchilar uchun",
                callback_data='worker'
            )
        ]
    ]
)


async def send_answers_keyboard(test_id, time):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Natijani yuborish",
                    callback_data=answers_keyboard_data.new(test_id=test_id, time=time)
                )
            ]
        ]
    )
    return markup
