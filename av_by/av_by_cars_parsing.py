import os
import platform
import subprocess
import sys

import requests
from bs4 import BeautifulSoup, SoupStrainer
from fake_useragent import UserAgent
import csv
import datetime

date = datetime.datetime.now().strftime('%d%m%Y')
URL = 'https://cars.av.by/volkswagen'
USER = UserAgent().random
HEADERS = {'user-agent': USER}
# CLASS_CONTENT = SoupStrainer(attrs={
#     'class': ['standart-view m-view result-explore'],
# })
FILE = f'../{date}_BY.csv'


def get_html(url, params=None):
    request = requests.get(url, headers=HEADERS, params=params)
    return request


# def get_pages_count(html):
#     soup = BeautifulSoup(html.text, 'html.parser')
#     pagination = soup.find_all('span', class_='page-item mhide')
#     if pagination:
#         return int(pagination[-1].get_text())
#     return 1

print(get_html(URL))

# def get_content(html):
#     pass
#
#
# def save_file(items, path):
#     with open(path, 'w', newline='') as file:
#         writer = csv.writer(file, )
#         writer.writerow(['Марка', 'Модель', 'Год', 'Двигатель', 'Пробег', 'Стоимость в долларах', 'Город', 'Ссылка', ])
#         for item in items:
#             writer.writerow([
#                 item['brand'],
#                 item['model'],
#                 item['year'],
#                 item['engine'],
#                 item['mileage'],
#                 item['price_dollars'],
#                 item['city'],
#                 item['link'],
#             ])
#
#
# def parse():
#     html = get_html(URL)
#     if html.status_code == 200:
#         pages_count = get_pages_count(html)
#         cars = []
#
#     else:
#         print('Error')