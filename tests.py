import pytest

import const
import database
import global_var
import parse


def test_city():
    """
    Функция на проверку того, что город всех вакансий - Москва
    """
    global_var.job = '/vospitatel'
    parse.parse()
    vacancy_list = database.get_data_dict()
    for vacancy in vacancy_list:
        place = vacancy[const.name_place_work]
        num_of_city = place.find("Москва")
        assert num_of_city == 0


def test_link():
    """
    Функция на проверку того, что ссылки на все вакансии имеют формат .html
    """
    global_var.job = '/vospitatel'
    parse.parse()
    vacancy_list = database.get_data_dict()
    for vacancy in vacancy_list:
        link = vacancy[const.name_link]
        num_of_format = link.find('.html')
        if num_of_format:
            num_of_format = True
        assert num_of_format is True


def test_name():
    """
    Функция на проверку того, что профессия вакансий нашлась
    """
    global_var.job = '/vospitatel'
    parse.parse()
    vacancy_list = database.get_data_dict()
    for vacancy in vacancy_list:
        name = vacancy[const.name_vacancy]
        if name != '':
            name = True
        assert name is True


def test_salary():
    """
    Функция на проверку того, что зарплата вакансий нашлась
    """
    global_var.job = '/vospitatel'
    parse.parse()
    vacancy_list = database.get_data_dict()
    for vacancy in vacancy_list:
        salary = vacancy[const.name_salary]
        if salary != '':
            salary = True
        assert salary is True


def test_company():
    """
    Функция на проверку того, что компания вакансий нашлась
    """
    global_var.job = '/vospitatel'
    parse.parse()
    vacancy_list = database.get_data_dict()
    for vacancy in vacancy_list:
        company = vacancy[const.name_company]
        if company != '':
            company = True
        assert company is True


def test_info():
    """
    Функция на проверку того, что информация о вакансиях нашлась
    """
    global_var.job = '/vospitatel'
    parse.parse()
    vacancy_list = database.get_data_dict()
    for vacancy in vacancy_list:
        info = vacancy[const.name_info]
        if info != '':
            info = True
        assert info is True
