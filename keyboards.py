from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, \
    KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from prs import URL
button_search_film = KeyboardButton('Искать фильм по названию 🎥')
button_search_person = KeyboardButton('Искать персону по имени 👨‍')
button_back_to_menu = KeyboardButton('Я передумал 😅')

menu_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(button_search_film, button_search_person)
back_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_back_to_menu)
#markup = InlineKeyboardMarkup().add(button_search_film).add(button_search_person)