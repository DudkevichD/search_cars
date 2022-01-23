import csv


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, )
        writer.writerow(['Марка', 'Модель', 'Год', 'Двигатель', 'Пробег', 'Стоимость в рублях', 'Город', 'Ссылка'])
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
