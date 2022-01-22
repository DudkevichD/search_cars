import csv
import datetime
import os
import platform
import subprocess
import sys

import requests
from bs4 import BeautifulSoup, SoupStrainer
from fake_useragent import UserAgent

date = datetime.datetime.now().strftime('%d%m%Y')
USER = UserAgent().random
HEADERS = {'user-agent': USER}
URL = 'https://www.avito.ru/rossiya/avtomobili/mercedes-benz-ASgBAgICAUTgtg3omCg?cd=1'
CLASS_CONTENT = SoupStrainer(attrs={
    'class': ['items-items-kAJAg'],
})
FILE = f'../{date}_RU.csv'

YEARS = [str(i) for i in range(1900, 2025)]
CAPACITY = [str(i / 10) for i in range(10, 70, 1)]


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
    soup = BeautifulSoup(html, 'html.parser', parse_only=CLASS_CONTENT)
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
                                class_='iva-item-text-Ge6dR text-text-LurtD text-size-s-BxGpL').get_text().split()

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
            'city': item.find('span', class_='geo-address-fhHd0 text-text-LurtD text-size-s-BxGpL').get_text().split()[
                -1],
            'link': url + item.find('a', class_='link-link-MbQDP').get('href'),
        })

    return cars


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, )
        writer.writerow(['Марка', 'Модель', 'Год', 'Двигатель', 'Пробег', 'Стоимость в рублях', 'Город', 'Ссылка', ])
        for item in items:
            writer.writerow([
                item['brand'],
                item['model'],
                item['year'],
                item['engine'],
                item['mileage'],
                item['price_dollars'],
                item['city'],
                item['link'],
            ])


def parse(URL):
    html = get_html(URL)
    if html.status_code == 200:
        pages_count = get_pages_count(html)
        cars = []
        if pages_count > 25:
            pages_count = 5
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
        print(html.status_code)


parse(URL)
