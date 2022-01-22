from auto_ria_com import auto_ria_ua_cars_parsing as ua
from avito_ru import avito_ru_cars_parsing as ru
URL = {
    'ua': {
        'wv': 'https://auto.ria.com/car/volkswagen/',
        'audi': 'https://auto.ria.com/car/audi/',
        'bmw': 'https://auto.ria.com/car/bmw/',
        'mb': 'https://auto.ria.com/car/mercedes-benz/',
    },
    'ru': {
        'wv': 'https://www.avito.ru/rossiya/avtomobili/volkswagen-ASgBAgICAUTgtg24mSg',
        'audi': 'https://www.avito.ru/rossiya/avtomobili/audi-ASgBAgICAUTgtg3elyg?cd=1',
        'bmw': 'https://www.avito.ru/rossiya/avtomobili/bmw-ASgBAgICAUTgtg3klyg?cd=1',
        'mb': 'https://www.avito.ru/rossiya/avtomobili/mercedes-benz-ASgBAgICAUTgtg3omCg?cd=1',
    },
    'by': {
        'wv': 'https://cars.av.by/volkswagen',
        'audi': 'https://cars.av.by/audi',
        'bmw': 'https://cars.av.by/bmw',
        'mb': 'https://cars.av.by/mercedes-benz',
    }
}


def get_selected_parsing(country='ua', brand='wv'):
    if country == 'ua':
        ua.parse(URL[country][brand])
    if country == 'ru':
        ru.parse(URL[country][brand])


get_selected_parsing()

