import requests
from bs4 import BeautifulSoup

import const
import database
import global_var


HEADERS = {'user-agent': const.user_agent,
           'accept': const.accept}
HOST = 'https://www.superjob.ru/vakansii'
SITE = 'https://www.superjob.ru'


def get_html(url, params=None):
    """
    Функция получения текста html по указанному url
    :param url:  ссылка на страницу
    :param params: параметры получения текста
    :return: текст html
    """
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_vacancy(html):
    """
    Функция поиска информации на сайте
    :param html: ссылка на страницу
    :return: список из всех вакансий
    """
    param_bs4 = 'html.parser'  # параметр для BeautifulSoup
    soup = BeautifulSoup(html, param_bs4)
    vacancy_class_type = 'div'
    vacancy_class = 'Fo44F QiY08 LvoDO'
    items = soup.find_all(vacancy_class_type, class_=vacancy_class)
    vacancy = []
    for item in items:
        salary_class_type = 'span'
        salary_class = '_1OuF_ _1qw9T f-test-text-company-item-salary'
        salary = item.find(salary_class_type, class_=salary_class)
        if salary:
            salary = salary.get_text().replace(const.change_symbol_from, const.change_symbol_to)
        else:
            salary = const.unknown

        company_class_type = 'span'
        company_class = '_1h3Zg _3Fsn4 f-test-text-vacancy-item-company-name e5P5i _2hCDz _2ZsgW _2SvHc'
        company = item.find(company_class_type, class_=company_class)
        if company:
            company = company.get_text()
        else:
            company = const.unknown

        info_class_type = 'span'
        info_class = '_1h3Zg _38T7m e5P5i _2hCDz _2ZsgW _2SvHc'
        info = item.find(info_class_type, class_=info_class)
        if info:
            info = info.get_text()
        else:
            info = const.unknown

        place_class_type = 'span'
        place_class = '_1h3Zg f-test-text-company-item-location '\
                      'e5P5i _2hCDz _2ZsgW'
        place = item.find(place_class_type, class_=place_class).get_text().\
            replace(const.change_symbol_from, const.change_symbol_to)
        city = "Москва"
        place = place[place.find(city):]  # Берем информацию о месте работы только начиная с города

        name_class_type = 'div'
        name_class = '_1h3Zg _u7Tv _2rfUm _2hCDz _21a7u _2rPTA'

        link_class_type = 'a'
        link_class = 'icMQ_'
        link_get = 'href'
        vacancy.append({
            'name': item.find(name_class_type, class_=name_class).get_text(),
            'link': SITE + item.find(link_class_type, class_=link_class).get(link_get),
            'salary': salary,
            'company': company,
            'place': place,
            'info': info
        })
    return vacancy


def parse():
    url = f'{HOST}{global_var.job}.html'
    first_element_of_file = 1  # с какого символа в слове job начинается название файла для базы данных
    file_job_name = global_var.job[first_element_of_file:]  # название файла для определенной профессии
    file_job = f'{file_job_name}.csv'
    html = get_html(url)
    status_success = 200
    status_fail = 'Error'
    if html.status_code == status_success:
        vacancy = get_vacancy(html.text)
        database.save_file(vacancy, file_job)
    else:
        print(status_fail)
