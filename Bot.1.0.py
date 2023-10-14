import openai
import telebot
from config import TELEGRAM_BOT_TOKEN, OPEN_API_KEY

openai.api_key = OPEN_API_KEY
token = TELEGRAM_BOT_TOKEN
bot = telebot.TeleBot(token)

# задаем модель и максимальное количество слов
model_engine = "text-davinci-003"
max_tokens = 3500

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