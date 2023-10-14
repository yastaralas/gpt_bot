import openai
import telebot
from config import TELEGRAM_BOT_TOKEN, OPEN_API_KEY, PARENTS

openai.api_key = OPEN_API_KEY
token = TELEGRAM_BOT_TOKEN
bot = telebot.TeleBot(token)

# задаем модель и максимальное количество слов
model_engine = "text-davinci-003"
max_tokens = 3500

# Ограничение в команде
@bot.message_handler(commands=['start'])
def start(message):
    parents = PARENTS
    if message.chat.id not in parents:
        bot.send_message(message.chat.id, 'Мама не разрешает разговаривать с незнакомцами.')
    else:
        bot.send_message(message.chat.id, 'Привет!\n\nО чем ты хочешь поговорить?')

# Ограничение доступа к боту по ID
parents = PARENTS
@bot.message_handler(func=lambda message: message.chat.id not in parents)
def some(message):
    bot.send_message(message.chat.id, 'Не дозволено общаться с незнакомцами.')

# переменная для хранения последнего сообщения и отправителя
last_messages = []

@bot.message_handler(func=lambda message: message.chat.id)
def handle_text(message):
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

    # Сохраняем последнее сообщение
    last_messages.append(message.text)

    # Ограничиваем список последних сообщений
    if len(last_messages) > 5:
        last_messages = last_messages[-5:]

# Запускаем бота
bot.polling()