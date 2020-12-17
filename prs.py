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
    items = soup.find('div', class_='item')
    if items.find_all('a', class_='search-page__title-link search-page__item-title-text'):
        url = (URL+items.find('a', class_='search-page__title-link search-page__item-title-text').get('href'))
        films_content['url'] = url
        films_content['name'] = items.find('a', class_='search-page__title-link search-page__item-title-text').text
        films_content['year'] = items.find('small', class_='cut_text').find_next().text
        films_content['genre'] = items.find('div', class_='search-page__genre-list').text
    return url


def get_film_content(url):
    page = get_html(url)
    page_soup = BeautifulSoup(page.text, 'lxml')
    films_content['country'] = page_soup.find('a', class_='film-page__country-link').text
    if page_soup.find('a', class_='noLink ratingsBlockKP'):
        films_content['rating'] = page_soup.find('a', class_='noLink ratingsBlockKP').find_next().text
    else:
        films_content['rating'] = ' '
    if page_soup.find('section', class_='text film-page__text'):
        films_content['description'] = page_soup.find('section', class_='text film-page__text').text
    else:
        films_content['description'] = page_soup.find('span', class_='text_hidden').text
    if page_soup.find('img', class_='movie_gallery_item movie_gallery_poster'):
        films_content['poster'] = page_soup.find('img', class_='movie_gallery_item movie_gallery_poster').get('src')
    elif page_soup.find('img', class_='serial_poster__main movie_gallery_item movie_gallery_poster'):
        films_content['poster'] = page_soup.find('img', class_='serial_poster__main movie_gallery_item movie_gallery_poster').get('src')
    else:
        films_content['poster'] = 'https://www.kino-teatr.ru/static/images/no_poster.jpg'
    print(films_content)
    return films_content


def search_film(s):
    s = s.replace('+', '%2B')
    s = s.replace(' ', '%20')
    s = '/search/?q=' + s
    html = get_html(URL+s)
    if html.status_code == 200:
        url = get_film_urls(html.text)
        return get_film_content(url)
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
    if person_soup.find('span', class_='age'):
        persons_content['age'] = person_soup.find('span', class_='age').text.replace('•', '').strip() + \
                             person_soup.find('a', {'itemprop': 'birthDate'}).text.strip()
    if person_soup.find('span', {'itemprop': 'deathDate'}):
        persons_content['age'] += person_soup.find('span', {'itemprop': 'deathDate'}).text.strip()
    profs = person_soup.find_all('li', {'itemprop': 'jobTitle'})
    persons_content['prof'] = [prof.find_next('span').text for prof in profs]
    if person_soup.find('a', {'data-original-url': re.compile('https://maps.google.com/maps')}):
        persons_content['country'] = person_soup.find('a', {'data-original-url': re.compile('https://maps.google.com/maps')}).text
    if person_soup.find('div', class_='textstart away-transparency_bottom'):
        persons_content['description'] = person_soup.find('div', class_='textstart away-transparency_bottom').find_next().text
    best_films = person_soup.find_all('a', class_='link-info-movie-type-film')
    persons_content['best_films'] = [URL+film.get('href') for film in best_films]
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

seacrh_person('нолан')