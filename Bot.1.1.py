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

# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(m):
    bot.send_message(m.chat.id, 'Привет!\n\nЯ отвечу на любой твой вопрос, но в контекст пока не умею.')

# задаем модель и максимальное количество слов
model_engine = "text-davinci-003"
max_tokens = 4000

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    prompt = message.text
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

# Запускаем бота
bot.polling(none_stop=True, interval=0)