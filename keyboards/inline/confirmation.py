from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

test_callback_data = CallbackData('test', 'confirm', 'test_id')

confirm_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Ha", callback_data="ok"),
            InlineKeyboardButton(text="❌ Yo'q", callback_data='cancel')
        ]
    ]
)


async def confirm_start_test_keyboard(test_id):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Ha", callback_data=test_callback_data.new(confirm='yes', test_id=test_id)),
                InlineKeyboardButton(text="❌ Yo'q", callback_data=test_callback_data.new(confirm='no', test_id=test_id))
            ]
        ]
    )
    return markup
