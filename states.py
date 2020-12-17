from aiogram.dispatcher.filters.state import State, StatesGroup


class Start_Menu(StatesGroup):
    start_menu = State()

class Choose_Func(StatesGroup):
    search_film = State()
    search_person = State()