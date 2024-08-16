from aiogram.dispatcher.filters.state import State, StatesGroup


class Post(StatesGroup):
    for_who = State()
    category_id = State()
    text = State()
    image = State()
    video = State()


class PostEditDelete(StatesGroup):
    id = State()
    text = State()
    image = State()
    video = State()
    edit = State()
