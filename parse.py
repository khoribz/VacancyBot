import requests
import csv
from bs4 import BeautifulSoup

import const


HEADERS = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/89.0.4389.90 Mobile Safari/537.36',
           'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
                     'image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
HOST = 'https://www.superjob.ru/vakansii'
SITE = 'https://www.superjob.ru'


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=' ')
        writer.writerow(['Вакансия', 'Зарплата', 'Компания', 'Место работы', 'Информация', 'Ссылка'])
        for item in items:
            writer.writerow([item['name'], item['salary'], item['company'],
                             item['place'], item['info'], item['link']])


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_vacancy(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='Fo44F QiY08 LvoDO')
    vacancy = []
    for item in items:
        salary = item.find('span', class_='_1OuF_ _1qw9T f-test-text-company-item-salary')
        if salary:
            salary = salary.get_text().replace('\xa0', ' ')
        else:
            salary = "Уточняйте"
        company = item.find('span', class_='_1h3Zg _3Fsn4 f-test-text-vacancy-item-company-name e5P5i _2hCDz _2ZsgW _2SvHc')
        if company:
            company = company.get_text()
        else:
            company = "Уточняйте"
        info = item.find('span', class_='_1h3Zg _38T7m e5P5i _2hCDz _2ZsgW _2SvHc')
        if info:
            info = info.get_text()
        else:
            info = "Уточняйте"
        place = item.find('span', class_='_1h3Zg f-test-text-company-item-location e5P5i _2hCDz _2ZsgW').get_text().replace('\xa0', ' ')
        place = place[place.find("Москва"):]
        vacancy.append({
            'name': item.find('div', class_='_1h3Zg _u7Tv _2rfUm _2hCDz _21a7u _2rPTA').get_text(),
            'link': SITE + item.find('a', class_='icMQ_').get('href'),
            'salary': salary,
            'company': company,
            'place': place,
            'info': info
        })
    return vacancy


def parse():
    URL = f'{HOST}{const.job}.html'
    FILE = f'{const.job[1:]}.csv'
    html = get_html(URL)
    if html.status_code == 200:
        vacancy = get_vacancy(html.text)
        save_file(vacancy, FILE)
    else:
        print('Error')
