import os
import platform
import subprocess
import sys

import requests
from bs4 import BeautifulSoup

from general_data.CONSTANTS import HEADERS, date
from general_data.save_file import save_file

YEARS = [str(i) for i in range(1900, 2025)]
CAPACITY = [str(i / 10) for i in range(10, 70, 1)]
FILE = f'../{date}_RU.csv'

def get_html(url, params=None):
    request = requests.get(url, headers=HEADERS, params=params)
    return request


def get_pages_count(html):
    soup = BeautifulSoup(html.text, 'html.parser')
    pagination = soup.find_all('span', class_='pagination-item-JJq_j')
    if pagination:
        return int(pagination[-2].get_text())
    return 1


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.findAll('div', class_='iva-item-content-rejJg')
    cars = []

    for item in items:
        url = 'https://www.avito.ru/'

        for year_ in item.find('h3', class_='title-root-zZCwT').get_text().split():
            if year_ in YEARS:
                year = year_
            else:
                year = '0000'

        description = item.find('div',
                                class_='iva-item-text-Ge6dR text-text-LurtD text-size-s-BxGpL'
                                ).get_text().split()

        engine = description[-1]
        for desc in description:
            if desc in CAPACITY:
                engine += ' ' + desc

        mileage = ''
        if 'км,' in description:
            if description[0] == 'Битый,':
                description.pop(0)
            for desc in description:
                if desc == 'км,':
                    break
                mileage += desc
        else:
            mileage = '0'

        prices = item.find(
            'span', class_='price-text-_YGDY text-text-LurtD text-size-s-BxGpL'
        ).get_text().split()
        price_dollars = ''
        for price in prices:
            if price.isdigit():
                price_dollars += price

        cars.append({
            'brand': item.find('h3', class_='title-root-zZCwT').get_text().split()[0],
            'model': item.find('h3', class_='title-root-zZCwT').get_text().split()[1].replace(",", ""),
            'year': year,
            'engine': engine,
            'mileage': mileage,
            'price_dollars': price_dollars,
            'city': item.find('span', class_='geo-address-fhHd0 text-text-LurtD text-size-s-BxGpL'
                              ).get_text().split()[-1],
            'link': url + item.find('a', class_='link-link-MbQDP').get('href'),
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
            os.startfile(f'..\{date}_RU.csv')

    else:
        print(html)
