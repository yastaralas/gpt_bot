TelegramBot
===========

Телеграмм Бот c GPT-3.

Требования и зависимости
---------
- Python 3.10
- Библиотека pyTelegramBotAPI (версия 4.10.0)
- Библиотека datetime (версия 5.2)
- Библиотека openai (версия 0.26.5)


Установка
---------

Создайте виртуальное окружение и активируйте его. Далее в виртуальном окружении выполните:

    pip install -r requirements.txt

Настройка
---------

Получите токен бота от BotFather в Telegram.
Создайте файл config.py и добавьте туда следующие настройки:


    TELEGRAM_BOT_TOKEN = 'Токен (API ключ) который получили от BotFather'
    OPEN_API_KEY = 'Токен (API ключ) который получили на сайте openai'
    PARENTS = [00000, 00000, 00000] # список из id пользователей, id можно узнать через бота @userinfobot

Запуск
------

В активированном виртуальном окружении выполните:

    python bot.2.1.py
