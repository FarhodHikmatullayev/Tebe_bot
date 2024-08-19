from aiogram.dispatcher.filters.state import State, StatesGroup


class Test(StatesGroup):
    answer = State()
    test_id = State()
