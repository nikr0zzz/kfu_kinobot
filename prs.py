import requests
from bs4 import BeautifulSoup

films_content = {}
HOST = 'https://ru.kinorium.com'
URL = 'https://ru.kinorium.com'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
           'accept': '*/*'}


def get_html(url, params=None):
    r = requests.get(url=url, headers=HEADERS, params=params)
    return r


def get_urls(html):
    global films_content
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find('div', class_='item')
    if items.find_all('a', class_='search-page__title-link search-page__item-title-text'):
        url = (HOST+items.find('a', class_='search-page__title-link search-page__item-title-text').get('href'))
        films_content['url'] = url
        films_content['name'] = items.find('a', class_='search-page__title-link search-page__item-title-text').text
        films_content['year'] = items.find('small', class_='cut_text').find_next().text
        films_content['genre'] = items.find('div', class_='search-page__genre-list').text
    return url


def get_content(url):
    page = get_html(url)
    page_soup = BeautifulSoup(page.text, 'html.parser')
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
    else:
        films_content['poster'] = page_soup.find('img', class_='serial_poster__main movie_gallery_item movie_gallery_poster').get('src')
    print(films_content)

    return films_content


def parse(s):
    s = s.replace('+', '%2B')
    s = s.replace(' ', '%20')
    s = '/search/?q=' + s
    html = get_html(URL+s)
    if html.status_code == 200:
        url = get_urls(html.text)
        return get_content(url)
    else:
        print('ERROR')



