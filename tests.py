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
        city = 'Москва'
        num_of_city = place.find(city)
        test_result = 0
        assert num_of_city == test_result


def test_link():
    """
    Функция на проверку того, что ссылки на все вакансии имеют формат .html
    """
    global_var.job = '/vospitatel'
    parse.parse()
    vacancy_list = database.get_data_dict()
    for vacancy in vacancy_list:
        link = vacancy[const.name_link]
        link_format = '.html'
        num_of_format = link.find(link_format)
        if num_of_format:  # если ссылка нашлась
            num_of_format = True
        test_result = True
        assert num_of_format == test_result


def test_name():
    """
    Функция на проверку того, что профессия вакансий нашлась
    """
    global_var.job = '/vospitatel'
    parse.parse()
    vacancy_list = database.get_data_dict()
    for vacancy in vacancy_list:
        name = vacancy[const.name_vacancy]
        empty_name = ''
        if name != empty_name:
            name = True
        test_result = True
        assert name == test_result


def test_salary():
    """
    Функция на проверку того, что зарплата вакансий нашлась
    """
    global_var.job = '/vospitatel'
    parse.parse()
    vacancy_list = database.get_data_dict()
    for vacancy in vacancy_list:
        salary = vacancy[const.name_salary]
        empty_salary = ''
        if salary != empty_salary:
            salary = True
        test_result = True
        assert salary == test_result


def test_company():
    """
    Функция на проверку того, что компания вакансий нашлась
    """
    global_var.job = '/vospitatel'
    parse.parse()
    vacancy_list = database.get_data_dict()
    for vacancy in vacancy_list:
        company = vacancy[const.name_company]
        empty_company = ''
        if company != empty_company:
            company = True
        test_result = True
        assert company == test_result


def test_info():
    """
    Функция на проверку того, что информация о вакансиях нашлась
    """
    global_var.job = '/vospitatel'
    parse.parse()
    vacancy_list = database.get_data_dict()
    for vacancy in vacancy_list:
        info = vacancy[const.name_info]
        empty_info = ''
        if info != empty_info:
            info = True
        test_result = True
        assert info == test_result
