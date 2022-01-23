import os
import platform
import subprocess
import sys

from bs4 import BeautifulSoup

from general_data.CONSTANTS import date
from general_data.get_html import get_html
from general_data.save_file import save_file
FILE = f'../{date}_UA.csv'

def get_pages_count(html):
    soup = BeautifulSoup(html.text, 'html.parser')
    pagination = soup.find_all('span', class_='page-item mhide')
    if pagination:
        return int(pagination[-1].get_text())
    return 1


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='content')
    cars = []
    for item in items:
        if item.find('li', class_='item-char js-race').get_text().split()[0].isdigit():
            mileage = int(item.find('li', class_='item-char js-race').get_text().split()[0] + '000')
        else:
            mileage = 0
        cars.append({
            'brand': item.find('span', class_='blue bold').get_text().split()[0],
            'model': item.find('span', class_='blue bold').get_text().split()[1],
            'year': item.find('a', class_='address').get_text().split()[-1],
            'engine': item.find_all('li', class_='item-char')[2].get_text(strip=True),
            'mileage': mileage,
            'price_dollars': int(item.find('span', class_='bold green size22').get_text().replace(" ", "")),
            'city': item.find('li', class_='item-char view-location js-location').get_text().split()[0],
            'link': item.find('a', class_='address').get('href'),
        })
    return cars


def parse(URL):
    html = get_html(URL)
    if html.status_code == 200:
        pages_count = get_pages_count(html)
        cars = []
        if pages_count > 10:
            pages_count = 10
        for page in range(1, pages_count + 1):
            print(f'Парсинг страницы {page} из {pages_count}...')
            html = get_html(URL, params={'page': page})
            cars.extend(get_content(html.text))
        save_file(cars, FILE)

        if platform.system() == 'Linux':
            opener = FILE if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, FILE])
        elif platform.system() == 'Windows':
            os.startfile(f'..\{date}_UA.csv')

    else:
        print('Error')
