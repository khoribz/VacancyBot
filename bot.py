import csv
import os.path
import telebot

import const
import jobs_name
import parse

bot = telebot.TeleBot(const.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.from_user.id, f'Добро пожаловать, {message.from_user.first_name}!\nЗдесь можно узнать о вакансиях\n'
                                           'Для поиска работы введите команду /help')


@bot.message_handler(commands=['help'])
def instruction(message):
    bot.send_message(message.from_user.id, '/search - Запуск поиска работы\n'
                                           '')


def show_jobs(message):
    const.number_of_messages = 3
    vacancy_list = get_data_dict()[const.number_of_vacancy: const.number_of_vacancy + const.number_of_messages]
    for vacancy in vacancy_list:
        vacancy_message = ''
        if const.number_of_messages == 0:
            break
        vacancy_message += 'Вакансия: ' + vacancy['Вакансия'] + '\n'
        vacancy_message += 'Зарплата: ' + vacancy['Зарплата'] + '\n'
        vacancy_message += 'Компания: ' + vacancy['Компания'] + '\n'
        vacancy_message += 'Место работы: ' + vacancy['Место работы'] + '\n'
        vacancy_message += 'Ссылка: ' + vacancy['Ссылка']
        const.number_of_messages -= 1
        bot.send_message(message.from_user.id, vacancy_message)
    const.number_of_vacancy += const.number_of_messages
    bot.send_message(message.from_user.id, "Для просмотра других вакансий введите /more\n"
                                           "Для поиска работы в других сферах введите /search")


@bot.message_handler(commands=list(jobs_name.dict_jobs.values()))
def chosen_job_parsing(message):
    # print(message.json['text'])
    const.job = message.json['text']
    if os.path.exists(f'{const.job}.csv'):
        show_jobs(message)
    else:
        parse.parse()
        show_jobs(message)


@bot.message_handler(commands=['search'])
def job_searching(message):
    bot.send_message(message.from_user.id, 'Выберете профессию:\n')
    choice = ''
    for job in jobs_name.dict_jobs:
        choice += f'{job}  /{jobs_name.dict_jobs[job]}\n'
    bot.send_message(message.from_user.id, f'Выберете профессию:\n{choice}')
    const.number_of_vacancy = 1


@bot.message_handler(commands=["more"])
def show_more(message):
    show_jobs(message)


def get_data_dict():
    vacancy_block = []
    with open(f'{const.job[1:]}.csv', 'r') as data_file:
        reader = csv.DictReader(data_file, delimiter=' ')
        for row in reader:
            vacancy_block.append(row)
    # print(vacancy_block)
    return vacancy_block


bot.polling(none_stop=True)
