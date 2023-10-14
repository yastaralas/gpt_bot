import openai
import telebot
import datetime
from config import TELEGRAM_BOT_TOKEN, OPEN_API_KEY, PARENTS


logfile = str(datetime.date.today()) + '.log' # формируем имя лог-файла

openai.api_key = OPEN_API_KEY
token = TELEGRAM_BOT_TOKEN
bot = telebot.TeleBot(token)

# задаем модель и максимальное количество слов
model_engine = "text-davinci-003" 
max_tokens = 3500

# ограничение в команде
@bot.message_handler(commands=['start'])
def start(message):
    parents = PARENTS # список из id пользователей
    if message.chat.id not in parents:
        bot.send_message(message.chat.id, 'Мама не разрешает разговаривать с незнакомцами.')
    else:
        bot.send_message(message.chat.id, 'Привет!\n\nО чем ты хочешь поговорить?')

# ограничение доступа к боту по ID
parents = PARENTS  # список из id пользователей
@bot.message_handler(func=lambda message: message.chat.id not in parents)
def some(message):
    bot.send_message(message.chat.id, 'Не дозволено общаться с незнакомцами.')

# переменная для хранения последнего сообщения и отправителя
last_messages = []

@bot.message_handler(func=lambda message: message.chat.id)
def handle_text(message):
    try:
        global last_messages
        prompt = ""
        # добавляем предыдущие сообщения в запрос
        if len(last_messages) > 0:
            prompt = "\n".join(last_messages[-5:]) + "\n"
        prompt += message.text

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


    # сохраняем последнее сообщение
    last_messages.append(message.text)

    # ограничиваем список последних сообщений
    if len(last_messages) > 5:
        last_messages = last_messages[-5:]

# запускаем бота
bot.polling()