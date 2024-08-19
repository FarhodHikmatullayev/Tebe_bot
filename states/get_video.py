from aiogram.dispatcher.filters.state import State, StatesGroup


class Video(StatesGroup):
    video = State()
