import telebot
from openai import OpenAI
from gtts import gTTS
import os
import time

# Инициализация клиента API OpenAI с вашим API ключом
client = OpenAI(
    api_key="вводим ключ API от OpenAI",
    base_url="https://api.proxyapi.ru/openai/v1",
)

# Инициализация бота с токеном вашего Telegram бота
bot = telebot.TeleBot("вводим токен бота")


@bot.message_handler(func=lambda message: True)
def chat_with_ai(message):
    chat_id = message.chat.id
    user_message = message.text

    messages = [{"role": "user", "content": user_message}]

    # Отправка запроса в нейронную сеть
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages
    )

    # Вывод ответа нейросети
    response_message = chat_completion.choices[0].message.content
    bot.send_message(chat_id, f"AI: {response_message}")

    # Преобразование текста ответа в аудиосообщение
    tts = gTTS(text=response_message, lang='ru')
    tts.save("response.mp3")

    # Отправка аудиосообщения пользователю
    audio = open("response.mp3", "rb")
    bot.send_voice(chat_id, audio)

    audio.close()  # Закрытие файла

    # Задержка перед удалением файла
    time.sleep(5)  # Задержка в 5 секунд (может потребоваться изменить значение)

    # Удаление временного аудиофайла
    os.remove("response.mp3")


# Запуск бота
bot.polling(none_stop=True, interval=0)
