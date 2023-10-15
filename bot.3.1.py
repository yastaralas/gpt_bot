import openai
import telebot
import datetime
from config import TELEGRAM_BOT_TOKEN, OPEN_API_KEY, PARENTS, PATTERN1
import re
import random


openai.api_key = OPEN_API_KEY
token = TELEGRAM_BOT_TOKEN
bot = telebot.TeleBot(token)

logfile = str(datetime.date.today()) + '.log' # формируем имя лог-файла

# задаем модель и максимальное количество слов
model_engine = "text-davinci-003"
max_tokens = 3500

# Ограничение в команде
@bot.message_handler(commands=['start'])
def start(message):
    parents = PARENTS # список из id пользователей
    if message.chat.id not in parents:
        bot.send_message(message.chat.id, 'Мама не разрешает разговаривать с незнакомцами.')
    else:
        bot.send_message(message.chat.id, 'Привет!\n\nО чем ты хочешь поговорить?')

# Ограничение доступа к боту по ID
parents = PARENTS  # список из id пользователей
@bot.message_handler(func=lambda message: message.chat.id not in parents)
def some(message):
    bot.send_message(message.chat.id, 'Не дозволено общаться с незнакомцами.')

# Инициализируйте переменные для хранения последнего сообщения и отправителя
last_messages = []

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        
    # Проверяем наличие и соответствие первому регулярному выражению
        pattern1 = PATTERN1
        match1 = re.search(pattern1, message.text, re.IGNORECASE)
        if match1:
            responses = ['Не хочу об этом говорить.', 'Давайте сменим тему.', 'Поговорим о чем-нибудь другом? Как погодка?']
            random_response = random.choice(responses)
            bot.send_message(message.chat.id, random_response)
       

 # Проверяем наличие и соответствие второму регулярному выражению
        pattern2 = r'(ка*к\s*т\wбя\s*з\wвут|ка*к\s*тв\w\w\s*им\w|у\s*т\wбя\s*есть\s*им\w|т\wбя\s*как\s*з\wвут)'
        match2 = re.search(pattern2, message.text, re.IGNORECASE)
        if match2:
            bot.send_message(message.chat.id, 'У меня нет имени.')


        patterns = [
            PATTERN1,
            r'(ка*к\s*т\wбя\s*з\wвут|ка*к\s*тв\w\w\s*им\w|у\s*т\wбя\s*есть\s*им\w|т\wбя\s*как\s*з\wвут)',
        ]

    # Удалить регулярные выражения из текста сообщения
        cleaned_text = message.text
        for pattern in patterns:
            cleaned_text = re.sub(pattern, '', cleaned_text, flags=re.IGNORECASE)

    # Добавить очищенный текст к промпту
        global last_messages
        last_messages.append(cleaned_text)
        if len(last_messages) > 5:
            last_messages = last_messages[-5:]
        prompt = "\n".join(last_messages)

        completion = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=0.5,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        bot.send_message(message.chat.id, completion.choices[0].text)
    except Exception as e:
        bot.send_message(message.from_user.id,  "Произошли технические шоколадки.")
        print(e)
        with open(logfile, 'a', encoding='utf-8') as f:
            f.write(str(datetime.datetime.today().strftime("%H:%M:%S")) + ':' + str(message.from_user.id) + ':' + str(message.from_user.first_name) + '_' + str(message.from_user.last_name) + ':' + str(message.from_user.username) +':'+ str(message.from_user.language_code) +':' + str(e) + '\n')


     # Сохраняем последнее сообщение
    last_messages.append(message.text)

    # Ограничиваем список последних сообщений
    if len(last_messages) > 5:
        last_messages = last_messages[-5:]

# Запускаем бота
bot.polling()
