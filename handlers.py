from aiogram import types
from aiogram.utils.markdown import text, bold, italic, code, pre, hbold
from aiogram.dispatcher.filters import Command
from bot import dp, bot
import states
import keyboards as kb
import prs


def get_film_caption(film):
    caption = hbold(film['name'] + ' ' + film['year'] + '\n' + ', '.join(film['genre']) + '\n' + ', '.join(film['country'])) + '\n' + \
              film['description'].strip() + '\n' + hbold(film['rating'])
    return caption


def get_person_caption(person):
    caption = hbold(person['name'] +'\n' + person['age'] + '\n' + ", ".join(person['prof']) + '\n') + "".join(person['description']) +\
              '\n'+'⬇️ЛУЧШИЕ ФИЛЬМЫ⬇️'
    return caption


@dp.callback_query_handler(lambda call: True, state=states.Film_Menu.person_ready)
async def film_callback(call: types.CallbackQuery):
    film = prs.get_film_content(call.data)
    caption = get_film_caption(film)
    link_kb = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('ПЕРЕЙТИ', url=film['url']))
    await bot.answer_callback_query(call.id)
    await bot.send_photo(call.from_user.id,photo=film['poster'], caption=caption, parse_mode=types.ParseMode.HTML, reply_markup=link_kb)


@dp.message_handler(Command("start"), state=None)
async def menu(message: types.Message):
    await message.answer('Привет я КиноБот помогу найти тебе фильмы и сериалы !', reply_markup=kb.menu_kb)
    await message.answer_sticker(r'CAACAgIAAxkBAAEBsHpf21oHoV4JvJETw9PIdBogMQRI3wACIAADDbbSGVmjiNFDIa13HgQ')
    await states.Start_Menu.start_menu.set()

@dp.message_handler(lambda msg: msg.text in kb.button_search_film.text, state=states.Start_Menu.start_menu)
async def find_fllm(message: types.Message):
    await message.answer('Введите название фильма', reply_markup=kb.back_kb)
    await states.Choose_Func.search_film.set()


@dp.message_handler(lambda msg: msg.text in kb.button_search_person.text, state=states.Start_Menu.start_menu)
async def find_person(message: types.Message):
    await message.answer('Введите название персоны', reply_markup=kb.back_kb)
    await states.Choose_Func.search_person.set()

@dp.message_handler(lambda msg: msg.text in kb.button_back_to_menu.text, state=[states.Choose_Func.search_film, states.Film_Menu.film_ready,states.Film_Menu.person_ready])
async def back_to_menu(message: types.Message):
    await message.answer('Подумай над выбором', reply_markup=kb.menu_kb)
    await states.Start_Menu.start_menu.set()


@dp.message_handler(lambda msg: msg.text in kb.button_add_to_favor.text, state=states.Choose_Func.search_film)
async def add_to_favor(message: types.Message):
    await message.answer('Добавлено в избранное !')
    await states.Film_Menu.go_to_favor.set()


@dp.message_handler(state=states.Choose_Func.search_film)
async def searching_film(message: types.Message):
    film_name = message.text
    film = prs.search_film(film_name)
    caption = get_film_caption(film)
    await message.reply_photo(film['poster'], caption=caption, parse_mode=types.ParseMode.HTML, reply_markup=kb.search_film_menu_kb)
    await states.Film_Menu.film_ready.set()


@dp.message_handler(state=states.Choose_Func.search_person)
async def searching_person(message: types.Message):
    person_name = message.text
    person = prs.seacrh_person(person_name)
    link_kb = types.InlineKeyboardMarkup()
    link_kb.add(types.InlineKeyboardButton(text=person['best_films_names'][0], callback_data=person['best_films_urls'][0]))
    link_kb.add(types.InlineKeyboardButton(text=person['best_films_names'][1], callback_data=person['best_films_urls'][1]))
    link_kb.add(types.InlineKeyboardButton(text=person['best_films_names'][2], callback_data=person['best_films_urls'][2]))
    caption = get_person_caption(person)
    await message.reply_photo(person['photo'], caption=caption, parse_mode=types.ParseMode.HTML, reply_markup=link_kb)
    await states.Film_Menu.person_ready.set()


@dp.message_handler(lambda msg: msg.text in kb.button_back_to_search_film.text, state=states.Film_Menu.film_ready)
async def re_searching_film(message: types.Message):
    await message.answer('Введите название фильма, но сначала хорошо подумайте !')
    await states.Choose_Func.search_film.set()


@dp.message_handler(lambda msg: msg.text in kb.button_back_to_search_person.text, state=states.Film_Menu.person_ready)
async def re_searching_film(message: types.Message):
    await message.answer('Введите имя персоны, но сначала хорошо подумайте !')
    await states.Choose_Func.search_person.set()
