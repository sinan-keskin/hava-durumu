import os
import requests
import telebot
from datetime import datetime

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_GROUP_ID = os.getenv("TELEGRAM_GROUP_ID")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def get_weather_data(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric&lang=tr"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def generate_comment(weather_id, temp):
    # Hava durumu kodlarına göre geniş kapsamlı yorumlar
    if 200 <= weather_id < 300: return "Fırtınalı bir hava var, çok dikkatli ol! ⚡🌩️"
    elif 300 <= weather_id < 600: return "Yağmurlu bir gün, şemsiyeni yanına almayı unutma! ☔🌧️"
    elif 600 <= weather_id < 700: return "Kar yağışı var, sıkı giyin ve kaymamaya dikkat et! ❄️☃️"
    elif 700 <= weather_id < 800: return "Hava biraz puslu veya sisli, görüş mesafesine dikkat! 🌫️"
    elif weather_id == 800:
        if temp > 25: return "Güneşli ve sıcak bir gün! İnce giyinmeyi tercih et. ☀️😎"
        elif temp < 10: return "Güneşli ama hava soğuk, sıkı giyinmeyi unutma! ☀️🥶"
        else: return "Harika, açık ve güneşli bir gün! ☀️"
    elif 801 <= weather_id <= 804:
        if temp < 10: return "Bulutlu ve soğuk, mutlaka kalın giyinmelisin. ☁️🧣"
        else: return "Hava parçalı bulutlu, huzurlu bir gün! ⛅"
    else: return "Hava durumu biraz değişken, tedbirli olmanı öneririm. 🧥"

def main():
    today_str = datetime.now().strftime('%d.%m.%Y')
    message = f"Günaydın! 🌅 Bugün ({today_str}):\n\n"
    
    for city in ["Ankara", "Istanbul"]:
        try:
            data = get_weather_data(city)
            weather_id = data["weather"][0]["id"]
            temp = round(data["main"]["temp"])
            desc = data["weather"][0]["description"].capitalize()
            comment = generate_comment(weather_id, temp)
            
            # Detaylı ve düzenli mesaj formatı
            message += f"📍 {city}: {desc}, {temp}°C\n💡 {comment}\n\n"
        except Exception as e:
            message += f"📍 {city}: Veri alınamadı 😔\n\n"
            
    bot.send_message(TELEGRAM_GROUP_ID, message)

if __name__ == "__main__":
    main()
