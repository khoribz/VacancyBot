# Telegram bot for job search in Moscow

This bot offers a choice of profession, which is used to search for vacancies
on the site *https://www.superjob.ru*

To launch the bot, you need to register the following commands in the console:
``` bash
git clone https://github.com/khoribz/review2.git -b dev
cd review2
pip3 install -r requirements.txt
python3 bot.py;
```
Now you can find a Telegram bot @GetVacancyBot and look for a job)


_bot.py_ - a file containing the main functions used when interacting with the bot   
_parse.py_ - a file in which information about vacancies is searched depending on the chosen profession   
_database.py_ - a file containing functions that work with databases   
_const.py_ - a file containing constants   
_global_var.py_ - a file containing global variables   
_jobs_name.py_ - a file containing a dictionary of the profession and its part of the address on the site 
_tests.py_ - a file containing tests of the site parsing results  
_requirements.txt_ - project launch requirements  
__Profile_ - the file needed to connect the bot to the Heroku server

# Bot commands:
_/start_ - start the bot   
_/help_ - further instructions after the start  
_/search_ - a command to show professions for which vacancies can be found
_/more_ - show more vacancies for the chosen profession 

# Testing:
To test the results of site parsing, it is necessary, while in the directory with the project,
to register the following command in the console:
``` bash
pytest tests.py
```