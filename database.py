import csv

import const
import global_var


def save_file(items, file_name):
    """
    Функция создания базы данных по информации, найденной на сайте
    :param items: найденные вакансии
    :param file_name: название файла базы данных
    :return:
    """
    newline_param = ''  # параметр newline для записи данных
    with open(file_name, 'w', newline=newline_param) as file:
        delimiter_param = ' '  # параметр разделения строк
        writer = csv.writer(file, delimiter=delimiter_param)
        writer.writerow([const.name_vacancy, const.name_salary,
                         const.name_company, const.name_place_work,
                         const.name_info, const.name_link])
        for item in items:  # записываем вакансию в строку по ее основным характеристикам
            writer.writerow([item['name'], item['salary'], item['company'],
                             item['place'], item['info'], item['link']])


def get_data_dict():
    """
    Функция получения листа вакансий, элемент листа - словарь из названия столбца и его значения
    :return: листа вакансий
    """
    vacancy_block = []
    first_element_of_file = 1  # с какого символа в слове job начинается название файла для базы данных
    file_job_name = global_var.job[first_element_of_file:]  # название файла для определенной профессии
    file_job = f'{file_job_name}.csv'
    with open(file_job, 'r') as data_file:
        delimiter_param = ' '  # параметр считывания базы данных, он устанавливался еще при ее создании
        reader = csv.DictReader(data_file, delimiter=delimiter_param)
        for row in reader:
            vacancy_block.append(row)
    return vacancy_block
