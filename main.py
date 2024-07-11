import telebot
from openai import OpenAI
from gtts import gTTS
import os
import time
import tempfile
import logging
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

# Получение переменных окружения
openai_api_key = os.getenv('OPENAI_API_KEY')
telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')

if openai_api_key is None:
    raise ValueError("Не удалось найти переменную OPENAI_API_KEY в окружении")

# Инициализация клиента OpenAI с использованием API ключа
client = OpenAI(api_key=openai_api_key)

# Настройка логирования
logging.basicConfig(level=logging.INFO)

@bot.message_handler(func=lambda message: True)
def chat_with_ai(message):
    try:
        chat_id = message.chat.id
        user_message = message.text
        logging.info(f"Сообщение от пользователя: {user_message}")

        # Получение ответа от OpenAI
        response_message = get_ai_response(user_message)

        # Отправка текстового сообщения
        bot.send_message(chat_id, f"AI: {response_message}")

        # Создание и отправка аудиосообщения
        send_audio_response(chat_id, response_message)

    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")
        bot.send_message(chat_id, "Произошла ошибка. Попробуйте еще раз.")

def get_ai_response(user_message):
    messages = [{"role": "user", "content": user_message}]
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages
    )
    return chat_completion.choices[0].message.content

def send_audio_response(chat_id, response_message):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        tts = gTTS(text=response_message, lang='ru')
        tts.save(temp_audio.name)

        # Отправка аудиосообщения пользователю
        with open(temp_audio.name, "rb") as audio:
            bot.send_voice(chat_id, audio)

        # Удаление временного аудиофайла
        os.remove(temp_audio.name)

# Запуск бота
bot.polling(none_stop=True, interval=0)

