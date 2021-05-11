import os.path
import telebot

import const
import database
import global_var
import jobs_name
import parse

bot = telebot.TeleBot(const.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    """
    Функция старта бота
    :param message: сообщение пользователя
    """
    start_message = f'Добро пожаловать, {message.from_user.first_name}!\n'\
                    'Здесь можно узнать о вакансиях\n'\
                    'Для информации введите команду /help'
    bot.send_message(message.from_user.id, start_message)


@bot.message_handler(commands=['help'])
def instruction(message):
    """
    Функция, срабатывающая на команду help, дает информацию о дальнейших действиях
    :param message: сообщение пользователя
    """
    help_message = '/search - Запуск поиска работы\n' \
                   'После этого будут предложены профессии вместе с командой, которую Вам следует нажать'
    bot.send_message(message.from_user.id, help_message)


def show_jobs(message):
    """
    Функция показа вакансий в боте
    :param message: сообщение пользователя
    """
    vacancy_list = database.get_data_dict()[global_var.number_of_vacancy:
                                            global_var.number_of_vacancy + global_var.number_of_messages]
    # vacancy_list = лист из const.number_of_messages вакансий, начиная с номера const.number_of_vacancy
    for vacancy in vacancy_list:
        # формирование сообщения для вывода вакансии в боте
        vacancy_message = ''
        if global_var.number_of_messages == 0:  # если вывели определенное число сообщений, останавливаемся
            break
        enter = '\n'
        vacancy_message += const.bold_name_vacancy + vacancy[const.name_vacancy] + enter
        vacancy_message += const.bold_name_salary + vacancy[const.name_salary] + enter
        vacancy_message += const.bold_name_company + vacancy[const.name_company] + enter
        vacancy_message += const.bold_name_place_work + vacancy[const.name_place_work] + enter
        vacancy_message += const.bold_name_info + vacancy[const.name_info] + enter
        vacancy_message += const.bold_name_link + vacancy[const.name_link]
        formed_vacancy = 1  # сформировали одну вакансию
        global_var.number_of_messages -= formed_vacancy  # отнимаем количество сформированных вакансий
        parse_mode_type = "Markdown"
        bot.send_message(message.from_user.id, vacancy_message, parse_mode=parse_mode_type)
    global_var.number_of_messages = 3  # количество выводимых вакансий
    global_var.number_of_vacancy += global_var.number_of_messages  # увеличиваем номер первой выводимой вакансии
    # по данной профессии
    show_jobs_message = "Для просмотра других вакансий введите /more\n"\
                        "Для поиска работы в других сферах введите /search"
    bot.send_message(message.from_user.id,  show_jobs_message)


@bot.message_handler(commands=list(jobs_name.dict_jobs.values()))
def chosen_job_parsing(message):
    """
    :param message: сообщение пользователя
    """
    global_var.number_of_vacancy = 0  # счетчик для текущей вакансии по данной профессии
    job_choice_message_before = "Поиск..."
    bot.send_message(message.from_user.id, job_choice_message_before)
    user_choice = 'text'
    global_var.job = message.json[user_choice]  # получаем команду, выбранную пользователем
    first_element_of_file = 1  # с какого символа в слове job начинается название файла для базы данных
    file_job_name = global_var.job[first_element_of_file:]  # название файла для определенной профессии
    file_job = f'{file_job_name}.csv'
    if os.path.exists(file_job):  # если база данных по данной профессии уже есть, берем вакансии оттуда
        show_jobs(message)
    else:  # иначе, парсим сайт, создаем бд, показываем вакансии
        parse.parse()
        show_jobs(message)


@bot.message_handler(commands=['search'])
def job_searching(message):
    """
    Функция, срабатывающая на команду search. Показываются все профессии, по которым доступны вакансии
    :param message: сообщение пользователя
    """
    if global_var.job:  # если уже вызывали команду /search, удаляем базу данных по прошлому запросу
        database.file_delete()
    point_of_job = ''  # строка сообщения с видом профессии и командой, вызывающей поиск вакансий
    for job in jobs_name.dict_jobs:  # перебираем все профессии из словаря и генерируем команду к ней
        line = f'{job}  /{jobs_name.dict_jobs[job]}\n'
        point_of_job += line
    search_message = f'Выберите профессию:\n{point_of_job}'
    bot.send_message(message.from_user.id, search_message)


@bot.message_handler(commands=["more"])
def show_more(message):
    """
    Функция для показа других вакансий по данной профессии
    :param message: сообщение пользователя
    """
    if global_var.number_of_vacancy >= len(database.get_data_dict()):
        vacancy_end_message = "Самые свежие объявления закончились, сделайте запрос чуть-чуть попозже)\n" \
                              "Для поиска вакансий по другим профессиям введите /search"
        bot.send_message(message.from_user.id, vacancy_end_message)
    else:
        show_jobs(message)


bot.polling(none_stop=True)
