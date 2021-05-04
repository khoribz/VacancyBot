import telebot

import const
import parse


TOKEN = '1628079242:AAFRgOko-BVHmI9ai299WJz8R-0tPBmhebs'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def welcome(message):
    bot.reply_to(message, f'Добро пожаловать, {message.from_user.first_name}!\nЗдесь можно узнать о вакансиях\n'
                          'Чтобы продолжить, введите команду /search\n'
                          'Для показа функционала введите команду /help')

def show_jobs(message):
    for vacancy in range(const.number_of_vacancy, const.number_of_messages + const.number_of_vacancy):
        bot.send_message(message.from_user.id, f"{const.file_lines[vacancy]}")
    const.number_of_vacancy += const.number_of_messages
    bot.send_message(message.from_user.id, "Для просмотра других вакансий введите /more")

@bot.message_handler(commands=["search"])
def job_searching(message):
    parse.parse()
    show_jobs(message)

@bot.message_handler(commands=["more"])
def show_more(message):
    show_jobs(message)


bot.polling(none_stop=True)
