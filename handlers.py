from aiogram import types
from aiogram.utils.markdown import text, bold, italic, code, pre, hbold
from aiogram.dispatcher.filters import Command
from bot import dp
import states
import keyboards as kb
import prs


def get_caption(film):
    caption = hbold(film['name'] + film['year'] +'\n(' + film['genre'] + ')  |'+film['country']+'\n')
    if str(film['description']).startswith(' Описание'):
        film['description'] = str(film['description']).replace('Описание', '').strip()
    caption += film['description']+'\n'
    caption += hbold('Оценка на КиноПоиске: '+film['rating'])
    print(caption)
    return caption

@dp.message_handler(Command("start"), state=None)
async def menu(message: types.Message):
    await message.answer('Привет я КиноБот помогу найти тебе фильмы и сериалы !', reply_markup=kb.menu_kb)
    await message.answer_sticker(r'CAACAgIAAxkBAAEBsHpf21oHoV4JvJETw9PIdBogMQRI3wACIAADDbbSGVmjiNFDIa13HgQ')
    await states.Start_Menu.start_menu.set()


@dp.message_handler(lambda msg: msg.text in kb.button_back_to_menu.text, state=[states.Choose_Func.search_film, states.Choose_Func.search_person])
async def back_to_menu(message: types.Message):
    await message.answer('Подумай над выбором', reply_markup=kb.menu_kb)
    await states.Start_Menu.start_menu.set()

@dp.message_handler(lambda msg: msg.text in kb.button_search_film.text, state=states.Start_Menu.start_menu)
async def find_fllm(message: types.Message):
    await message.answer('Введите название фильма', reply_markup=kb.back_kb)
    await states.Choose_Func.search_film.set()


@dp.message_handler(state=states.Choose_Func.search_film)
async def searching_film(message: types.Message):
    film_name = message.text
    film = prs.search_film(film_name)
    caption = get_caption(film)
    link_kb = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('ПЕРЕЙТИ', url=film['url']))
    await message.reply_photo(film['poster'], caption=caption, parse_mode=types.ParseMode.HTML, reply_markup=link_kb)

@dp.message_handler(lambda msg: msg.text in kb.button_search_person.text, state=states.Start_Menu.start_menu)
async def find_person(message: types.Message):
    await message.answer('Введите название персоны', reply_markup=kb.back_kb)
    await states.Choose_Func.search_person.set()

