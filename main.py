import os
import requests
import telebot
from datetime import datetime

# Secrets'tan verileri alıyoruz
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_GROUP_ID = os.getenv("TELEGRAM_GROUP_ID")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def get_weather_data(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric&lang=tr"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def main():
    today_str = datetime.now().strftime('%d.%m.%Y')
    message = f"Günaydın! 🌅 İşte bugünün hava durumu raporu ({today_str}):\n\n"
    
    cities = ["Ankara", "Istanbul"]
    for city in cities:
        try:
            data = get_weather_data(city)
            temp = round(data["main"]["temp"])
            desc = data["weather"][0]["description"].capitalize()
            message += f"📍 {city}: {desc}, {temp}°C\n"
        except Exception as e:
            message += f"📍 {city}: Veri alınamadı 😔\n"
            
    # Mesajı Telegram grubuna gönder
    bot.send_message(TELEGRAM_GROUP_ID, message)
    print("Mesaj Telegram'a başarıyla gönderildi!")

if __name__ == "__main__":
    main()
