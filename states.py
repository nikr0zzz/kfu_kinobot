from aiogram.dispatcher.filters.state import State, StatesGroup


class Start_Menu(StatesGroup):
    start_menu = State()

class Choose_Func(StatesGroup):
    search_film = State()
    search_person = State()

class Film_Menu(StatesGroup):
    person_ready = State()
    go_to_favor = State()
    film_ready = State()
