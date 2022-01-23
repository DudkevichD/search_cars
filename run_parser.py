import argparse

from logic.logic import get_selected_parsing

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('country', help='Выбор страны Россия-"ru", Беларусь-"by", Ураина-"ua" ')
    parser.add_argument('brand', help='Выбор автомобиля , Volkswagen-"vw", Audi-"audi", BMW-"bmw", '
                                                    'Mercedes-Benz-"mb"')
    args = parser.parse_args()
    get_selected_parsing(args.country, args.brand)
