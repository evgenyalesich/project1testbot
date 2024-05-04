import os
import requests
import telebot
import logging
from bs4 import BeautifulSoup

token = os.getenv('TOKEN')
bot = telebot.TeleBot(token)


class WeatherForecast:
    def __init__(self):
        self.api_key = os.getenv('WEATHER_API')

    def get_weather(self, city, ):
        if not self.api_key:
            print("Отсутствует API ключ OpenWeatherMap. Установите переменную окружения WEATHER_API.")
            return

        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather_description = data['weather'][0]['description']
            icon = data['weather'][0]['icon']
            temperature = data['main']['temp']
            humidity = data['main']['humidity']
            wind_speed = data.get("wind", {}).get("speed", "Нет данных")

            icon_url = f"http://openweathermap.org/img/wn/{icon}.png"
            icon_data = requests.get(icon_url).content

            output = (
                f"Погода в городе {city}:\n"
                f"Описание: {weather_description}\n"
                f"Температура: {temperature} °C\n"
                f"Влажность: {humidity}%\n"
                f"Скорость ветра: {wind_speed} м/с"
                f"Описание: {weather_description}\n"

            )
            return output, icon_data
        else:
            return 'Не удалось получить данные о погоде.', None

class NewsParser:
    def __init__(self, news_url):
        self.news_url = news_url

    def parse_news(self):
        try:
            response = requests.get(self.news_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                news_list = []
                for news_item in soup.find_all('div', class_='news-item'):
                    title = news_item.find('h2').text.strip()
                    link = news_item.find('a')['href']
                    news_list.append({'title': title, 'link': link})
                return news_list
            else:
                print(f"Failed to retrieve news from {self.news_url}. Status code: {response.status_code}")
                return None
        except requests.RequestException as e:
            print(f"Error parsing news: {e}")
            return None

def process_selected_news(message, news_data):
    try:
        selected_index = int(message.text) - 1
        selected_news = news_data[selected_index]
        full_article = get_full_article(selected_news['link'])
        bot.send_message(message.chat.id, f"Вы выбрали: {selected_news['title']}\n\n{full_article}")
    except (ValueError, IndexError):
        bot.send_message(message.chat.id, "Некорректный выбор. Пожалуйста, выберите номер новости из списка.")

def get_full_article(link):
    try:
        
        pass
    except requests.RequestException as e:
        print(f"Error fetching full article: {e}")
        return "Не удалось получить полную статью."

# Define a function to process the weather request
def process_weather_request(message, city):
    weather_forecast = WeatherForecast()
    weather_data, icon_data = weather_forecast.get_weather(city)
    if icon_data:
        bot.send_photo(message.chat.id, icon_data)
    bot.send_message(message.chat.id, weather_data)

# Define a function to process the currency request
def process_currency_request(message):
    logger = logging.getLogger(__name__)
    logger.info(f"Processing currency request for code: {message.text}")
    currency_code = message.text.upper()
    # Add your currency_service functionality here

# Define a function to process the news request
def process_news_request(message):
    logger = logging.getLogger(__name__)
    logger.info("Processing news request")
    # Add your news_service functionality here

# Define a handler for the command /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button_weather = telebot.types.KeyboardButton('Получить погоду 🌤️')
    button_currency = telebot.types.KeyboardButton('Получить курс валют 💱')
    button_news = telebot.types.KeyboardButton('Новости дня 📰')
    button_order_bot = telebot.types.KeyboardButton('Заказать бот 🤖')

    # Customize button colors
    button_weather. color = 'primary'
    button_currency.color = 'primary'
    button_news.color = 'primary'
    button_order_bot.color = 'positive'  # Different color for the order button

    keyboard.add(button_weather, button_currency, button_news, button_order_bot)
    bot.send_message(message.chat.id, "Добро пожаловать! Выберите действие:", reply_markup=keyboard)
@bot.message_handler(func=lambda message: message.text == "Получить погоду 🌤️")
def handle_weather_request(message):
    bot.send_message(message.chat.id, "Введите название города:")
    bot.register_next_step_handler(message, process_weather)

# Define a function to process the user's city input for weather request
def process_weather(message):
    city = message.text
    process_weather_request(message, city)

# Define a handler for the "Получить курс валют" button
@bot.message_handler(func=lambda message: message.text == "Получить курс валют 💱")
def handle_currency_request(message):
    bot.send_message(message.chat.id, "Введите код валюты (например, USD, EUR):")
    bot.register_next_step_handler(message, process_currency_request)

# Define a handler for the "Новости дня" button
@bot.message_handler(func=lambda message: message.text == "Новости дня 📰")
def handle_news_request(message):
    process_news_request(message)

@bot.message_handler(func=lambda message: message.text == "Заказать бот 🤖")
def handle_order_bot_button(message):
    bot.send_message(message.chat.id, "Для заказа бота свяжитесь с нами по адресу ")
# Define a handler for any other message
@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    bot.send_message(message.chat.id, "Извините, я не понял ваш запрос. Пожалуйста, используйте кнопки.")

proxies = [
    '72.195.34.58 :4145',
    '187.102.238.49:999',
    
]

# Заголовок User-Agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}

# URL-адрес сайта
url = 'https://charter97.org/ru/news/p/1/'

# Цикл для выполнения запросов с использованием каждого прокси
for proxy in proxies:
    # Формирование словаря прокси для запроса
    proxy_dict = {
        'http': f'http://{proxy}',
        'https': f'https://{proxy}'
    }

    try:
        # Выполнение GET-запроса с использованием прокси и заголовка User-Agent
        response = requests.get(url, proxies=proxy_dict, headers=headers)

       

    except requests.RequestException as e:
        
        print(f'Произошла ошибка с прокси {proxy}: {e}')

# Start polling
bot.polling()