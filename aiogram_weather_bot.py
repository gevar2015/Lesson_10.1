import requests
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
import asyncio

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Ваш токен от BotFather
TOKEN = '7339699782:AAEL2Qhwr3_SKJhco56vWxUFqUZNDKHOdTg'
# Ваш API-ключ OpenWeatherMap
WEATHER_API_KEY = 'Вa7e004594fb3bfc77e40ef3ddc9ff369'

# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher()


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
    await message.answer("Привет, поговорим о погоде!")


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


# Главная функция запуска бота
async def main():
    # Запуск поллинга
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(main())
