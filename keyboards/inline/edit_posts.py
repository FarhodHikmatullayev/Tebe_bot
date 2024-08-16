from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

text_or_video_or_image = CallbackData('edit', 'post_id', 'text_video_image')


async def get_choose_button(post_id, video_image):
    if video_image == "image":
        text = "Rasm"
    elif video_image == "video":
        text = "Video"
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Text",
                    callback_data=text_or_video_or_image.new(post_id=post_id, text_video_image='text')
                ),
                InlineKeyboardButton(
                    text=text,
                    callback_data=text_or_video_or_image.new(post_id=post_id, text_video_image=video_image)
                )
            ],
            [
                InlineKeyboardButton(
                    text="Ikkisini ham",
                    callback_data=text_or_video_or_image.new(post_id=post_id, text_video_image='both')
                )
            ]
        ]
    )
    return markup
