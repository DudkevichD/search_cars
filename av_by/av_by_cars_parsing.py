import os
import platform
import subprocess
import sys
import math
from bs4 import BeautifulSoup

from general_data.CONSTANTS import date
from general_data.get_html import get_html
from general_data.save_file import save_file

FILE = f'../{date}_BY.csv'
URL = 'https://cars.av.by/filter?brands[0][brand]=1216'


def get_pages_count(html):
    soup = BeautifulSoup(html.text, 'html.parser')
    pagination_elements = soup.find('div', class_='paging__text').get_text().split()
    for element in pagination_elements:
        if element.isdigit():
            str_cars = int(element)
            break
        else:
            str_cars = 1
    total_cars = ''
    for element in pagination_elements[pagination_elements.index('из') + 1: len(pagination_elements)]:
        total_cars += element
    total_cars = int(total_cars)
    pagination = math.ceil(total_cars / str_cars)

    return pagination


def get_content(html):
    soup = BeautifulSoup(html.text, 'html.parser')
    items = soup.find_all('div', class_='listing-item listing-item--color listing-item--top')
    url = 'https://cars.av.by/'

    cars = []
    for item in items:
        description = item.find('div', class_='listing-item__params').get_text().split()
        mileage_params = item.find('div', class_='listing-item__params').find_next('span').get_text().split()
        mileage = mileage_params[0] + mileage_params[1]
        dollars_params = item.find('div', class_='listing-item__priceusd').get_text().split()
        price_dollars_list = list(filter(lambda x: x.isdigit(), dollars_params))
        price_dollars = ''
        for dollars in price_dollars_list:
            price_dollars += dollars

        cars.append({
            'brand': item.find('span', class_='link-text').get_text().split()[0],
            'model': item.find('span', class_='link-text').get_text().split()[1],
            'year': item.find('div', class_='listing-item__params').get_text().split()[0],
            'engine': description[4] + description[2],
            'mileage': mileage,
            'price_dollars': price_dollars,
            'city': item.find('div', class_='listing-item__location').get_text(),
            'link': url + item.find('a', class_='listing-item__link').get('href'),
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
            html = get_html(URL + f'&page={page}')
            cars.extend(get_content(html))
        save_file(cars, FILE)

        if platform.system() == 'Linux':
            opener = FILE if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, FILE])
        elif platform.system() == 'Windows':
            os.startfile(f'..\{date}_BY.csv')

    else:
        print('Error')

