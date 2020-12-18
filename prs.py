import requests
import re
from bs4 import BeautifulSoup

films_content = {}
persons_content = {}
URL = 'https://ru.kinorium.com'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
           'accept': '*/*'}


def get_html(url, params=None):
    r = requests.get(url=url, headers=HEADERS, params=params)
    return r


def get_film_urls(html):
    global films_content
    soup = BeautifulSoup(html, 'lxml')
    film_url = URL + soup.find('h3', class_='search-page__item-title link-info-movie').find_next('a', class_='search-page__title-link search-page__item-title-text').get('href')
    return get_film_content(film_url)


def get_film_content(url):
    film_page = get_html(url)
    film_soup = BeautifulSoup(film_page.text, 'lxml')
    films_content['url'] = url
    films_content['name'] = film_soup.find('h1', class_= 'film-page__title-text film-page__itemprop').text.strip()
    films_content['poster'] = film_soup.find('div', class_='movie_poster__wrapper').find_next('img').get('src')
    if film_soup.find('div', class_='movie_poster__wrapper movie_poster__wrapper_placeholder'):
        films_content['poster'] = 'https://www.kino-teatr.ru/static/images/no_poster.jpg'
    films_content['year'] = film_soup.find('span', class_='film-page__title-label').text.strip()
    countries = film_soup.find_all('a', class_='film-page__country-link')
    films_content['country'] = [country.text.strip() for country in countries]
    genres = film_soup.find_all('li', {'itemprop': 'genre'})
    films_content['genre'] = [genre.get('content') for genre in genres]
    if film_soup.find('a', class_='noLink ratingsBlockKP'):
        films_content['rating'] = "Оценка на КиноПоиске: " + film_soup.find('a', class_='noLink ratingsBlockKP').find_next('span', class_='value').text.strip()
    else:
        films_content['rating'] = "Нет оценки"
    if film_soup.find('section', class_='text film-page__text'):
        films_content['description'] = film_soup.find('section', class_='text film-page__text').text.strip()
        films_content['description'] = films_content['description'][9:]
    elif film_soup.find('section', class_='text film-page__text with_hidden_text more_text_available'):
        films_content['description'] = film_soup.find('section', class_='text film-page__text with_hidden_text more_text_available').text.strip()
        films_content['description'] = films_content['description'][9:]
    else:
        films_content['description'] = "Ожидается в прокате"
    print(films_content)
    return films_content

def search_film(s):
    s = s.replace('+', '%2B')
    s = s.replace(' ', '%20')
    s = '/search/?q=' + s
    html = get_html(URL+s)
    if html.status_code == 200:
       return get_film_urls(html.text)
    else:
        print('ERROR')


def get_person_urls(html):
    global persons_content
    soup = BeautifulSoup(html, 'lxml')
    person_url = URL + soup.find('h3', class_='link-info-persona-type-persona cut_text').find_next('a', class_='search-page__title-link').get('href')
    return get_person_content(person_url)


def get_person_content(url):
    person_page = get_html(url)
    person_soup = BeautifulSoup(person_page.text, 'lxml')
    persons_content['url'] = url
    persons_content['name'] = person_soup.find('div', class_='person-page__title-elements-wrap').text.strip()
    persons_content['photo'] = person_soup.find('div', class_='person_portrait').find_next('img').get('src')
    if person_soup.find('span', class_='age'):
        persons_content['age'] = person_soup.find('span', class_='age').text.replace('•', '').strip() + \
                             '\n' + person_soup.find('a', {'itemprop': 'birthDate'}).text.strip()
    if person_soup.find('span', {'itemprop': 'deathDate'}):
        persons_content['age'] += ' - ' + person_soup.find('span', {'itemprop': 'deathDate'}).text.strip()
    profs = person_soup.find_all('li', {'itemprop': 'jobTitle'})
    persons_content['prof'] = [prof.find_next('span').text.strip() for prof in profs]
    if person_soup.find('a', {'data-original-url': re.compile('https://maps.google.com/maps')}):
        persons_content['country'] = person_soup.find('a', {'data-original-url': re.compile('https://maps.google.com/maps')}).text
    if person_soup.find('div', class_='textstart away-transparency_bottom'):
        description = person_soup.find('div', class_='textstart away-transparency_bottom').find_all_next('p')
        persons_content['description'] = ''
        for i in range(5):
            persons_content['description'] += description[i].text
        persons_content['description'] = persons_content['description'][:300]
        idx = persons_content['description'].rfind('.')
        persons_content['description'] = persons_content['description'][:idx]
    best_films_urls = person_soup.find_all('a', class_='link-info-movie-type-film')
    best_films_names = person_soup.find('a', class_='link-info-movie-type-film').find_all_next('span', class_='title cut_text')
    persons_content['best_films_urls'] = [URL+film.get('href') for film in best_films_urls]
    persons_content['best_films_names'] = [name.text for name in best_films_names]
    print(persons_content)
    return persons_content

def seacrh_person(s):
    s = s.replace('+', '%2B')
    s = s.replace(' ', '%20')
    s = '/search/?q=' + s
    html = get_html(URL + s)
    if html.status_code == 200:
        return get_person_urls(html.text)
    else:
        print('ERROR')

