from auto_ria_com import auto_ria_ua_cars_parsing as ua
from avito_ru import avito_ru_cars_parsing as ru
from av_by import av_by_cars_parsing as by
URL = {
    'ua': {
        'vw': 'https://auto.ria.com/car/volkswagen/',
        'audi': 'https://auto.ria.com/car/audi/',
        'bmw': 'https://auto.ria.com/car/bmw/',
        'mb': 'https://auto.ria.com/car/mercedes-benz/',
    },
    'ru': {
        'vw': 'https://www.avito.ru/rossiya/avtomobili/volkswagen-ASgBAgICAUTgtg24mSg',
        'audi': 'https://www.avito.ru/rossiya/avtomobili/audi-ASgBAgICAUTgtg3elyg?cd=1',
        'bmw': 'https://www.avito.ru/rossiya/avtomobili/bmw-ASgBAgICAUTgtg3klyg?cd=1',
        'mb': 'https://www.avito.ru/rossiya/avtomobili/mercedes-benz-ASgBAgICAUTgtg3omCg?cd=1',
    },
    'by': {
        'vw': 'https://cars.av.by/filter?brands[0][brand]=1216',
        'audi': 'https://cars.av.by/filter?brands[0][brand]=6',
        'bmw': 'https://cars.av.by/filter?brands[0][brand]=8',
        'mb': 'https://cars.av.by/filter?brands[0][brand]=683',
    }
}


def get_selected_parsing(country='ua', brand='wv'):
    if country == 'ua':
        ua.parse(URL[country][brand])
    if country == 'ru':
        ru.parse(URL[country][brand])
    if country == 'by':
        by.parse(URL[country][brand])

