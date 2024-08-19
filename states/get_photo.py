from aiogram.dispatcher.filters.state import State, StatesGroup


class Photo(StatesGroup):
    photo = State()
