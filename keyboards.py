from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, \
    KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from prs import URL
button_search_film = KeyboardButton('Искать фильм по названию 🎥')
button_search_person = KeyboardButton('Искать персону по имени 👨‍')
button_back_to_menu = KeyboardButton('Возврат в меню 😅')
button_add_to_favor = KeyboardButton('Добавить в избранное ⭐️')
button_back_to_search_film = KeyboardButton('Искать другой фильм, сериал🎦')
button_back_to_search_person = KeyboardButton('Искать другую персону 😎')

menu_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(button_search_film, button_search_person)
back_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_back_to_menu)
search_film_menu_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(button_add_to_favor, button_back_to_search_film, button_back_to_menu)

