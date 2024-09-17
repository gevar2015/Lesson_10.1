import requests
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
import asyncio
import os
from googletrans import Translator  # Для перевода текста
from gtts import gTTS  # Для создания голосовых сообщений
import io

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Ваш токен от BotFather
from config import TOKEN

# Ваш API-ключ OpenWeatherMap
WEATHER_API_KEY = 'Вa7e004594fb3bfc77e40ef3ddc9ff369'

# Инициализация бота и переводчика
bot = Bot(token=TOKEN)
dp = Dispatcher()
translator = Translator()

# Создание папки для сохранения изображений, если её ещё нет
if not os.path.exists("IMG"):
    os.makedirs("IMG")


# Функция для получения прогноза погоды
async def get_weather(city: str):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru'

    try:
        response = requests.get(url, timeout=10)  # Устанавливаем тайм-аут 10 секунд
        response.raise_for_status()  # Проверка на успешный статус ответа (например, 200)
        data = response.json()
        temp = data['main']['temp']
        description = data['weather'][0]['description']
        return f"Температура: {temp}°C\nУсловия: {description}"
    except requests.exceptions.HTTPError as http_err:
        return f"Ошибка HTTP: {http_err}"
    except requests.exceptions.ConnectionError:
        return "Ошибка подключения. Проверьте ваше интернет-соединение."
    except requests.exceptions.Timeout:
        return "Ошибка: Превышено время ожидания ответа от сервера."
    except requests.exceptions.RequestException as err:
        return f"Произошла ошибка: {err}"


# Обработчик команды /start
@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer(f"Привет, поговорим о погоде!, {message.from_user.first_name}")


# Обработчик команды /help
@dp.message(Command("help"))
async def send_help(message: Message):
    await message.answer("Чем могу помочь?")


# Обработчик команды /weather
@dp.message(Command("weather"))
async def send_weather(message: Message):
    city = "Москва"
    weather_info = await get_weather(city)
    await message.answer(f"Погода в {city}:\n{weather_info}", parse_mode="HTML")


# Обработчик для получения и сохранения фото
@dp.message_handler(content_types=types.ContentType.PHOTO)
async def handle_photos(message: types.Message):
    photo = message.photo[-1]  # Получаем фото самого высокого качества
    photo_path = f"IMG/{photo.file_unique_id}.jpg"  # Уникальное имя файла
    await photo.download(photo_path)  # Сохраняем фото в папку IMG
    await message.answer("Фото сохранено!")


# Обработчик для перевода текста на английский
@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_translation(message: types.Message):
    translated_text = translator.translate(message.text, dest='en').text
    await message.answer(f"Перевод на английский: {translated_text}")


# Обработчик команды /voice, для отправки голосового сообщения
@dp.message(Command("voice"))
async def send_voice_message(message: Message):
    text = "Привет! Это голосовое сообщение, созданное с помощью бота."
    tts = gTTS(text=text, lang='ru')
    voice_file = io.BytesIO()  # Временный файл для хранения голосового сообщения
    tts.write_to_fp(voice_file)
    voice_file.seek(0)
    await message.answer_voice(voice_file)


# Главная функция запуска бота
async def main():
    # Запуск поллинга
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(main())
