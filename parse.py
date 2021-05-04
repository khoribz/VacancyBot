import requests
import csv
from bs4 import BeautifulSoup


URL = 'https://hh.ru/vacancies/podrabotka?L_is_autosearch=false&L_profession_id=50.1&area=1&clusters=true&' \
      'enable_snippets=true&no_magic=true&part_time=only_saturday_and_sunday&page=1'
HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/89.0.4389.90 Safari/537.36',
           'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/'
                     'apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
HOST = 'https://hh.ru'
FILE = 'vacancy.csv'


def save_file(items, path):
    with open(path, 'w', newline='\n') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerow(['Вакансия', "Ссылка", "Зарплата", "Город", "Информация"])
        for item in items:
            writer.writerow([item['name'], item['link'], item['salary'],
                             item['city'], item['info']])


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='vacancy-serp-item')
    # print(items)
    vacancy = []
    for item in items:
        info = item.find('div', class_='g-user-content')
        if info:
            info = info.get_text()
        else:
            info = "Уточняйте"
        salary = item.find('div', class_='vacancy-serp-item__sidebar')
        if salary:
            salary = salary.get_text().replace('\xa0', '')
        else:
            salary = "Уточняйте"
        # responsibility = item.find('div', data_qa_='vacancy-serp__vacancy_snippet_responsibility')
        # responsibility = item.find('div', class_='g-user-content')
        # # responsibility = item.find('div', attrs={'class': 'g-user-content', 'data-qa':
        # 'vacancy-serp__vacancy_snippet_responsibility'})
        # if responsibility:
        #     responsibility = responsibility.get_text
        # else:
        #     responsibility = "Условия работы уточняйте"
        # requirements = item.find(attrs_={'class': 'g-user-content', 'data-qa': 'vacancy-serp__vacancy_snippet_requirement'})
        # if requirements:
        #     requirements = requirements.get_text
        # else:
        #     requirements = "Требования уточняйте"
        vacancy.append({
            'name': item.find('div', class_='vacancy-serp-item__info').get_text(),
            'link': item.find('a', class_='bloko-link HH-LinkModifier').get('href'),
            'salary': salary,
            'city': item.find('span', class_='vacancy-serp-item__meta-info').get_text(),
            'info': info
            # 'responsibility': responsibility,
            # 'requirements': requirements
        })
    # print(vacancy)
    return vacancy


def parse():
    html = get_html(URL)
    # print(html.status_code)
    if html.status_code == 200:
        # print(html.text)
        vacancy = get_content(html.text)
        save_file(vacancy, FILE)
    else:
        print('Error')


parse()
