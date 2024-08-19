from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Botni ishga tushurish"),
            types.BotCommand("help", "Yordam"),
            types.BotCommand("start_test", "Testni boshlash"),
            types.BotCommand("get_photo_url", "Rasmning url manzilini olish, Faqat admin uchun"),
            types.BotCommand("get_video_url", "Videoning url manzilini olish, Faqat admin uchun"),
        ]
    )
