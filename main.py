import os
import requests
from instagrapi import Client
from datetime import datetime

# Çevre değişkenlerini alıyoruz
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
IG_SESSIONID = os.getenv("IG_SESSIONID")
INSTAGRAM_GROUP_ID = os.getenv("INSTAGRAM_GROUP_ID")

CITIES = ["Ankara", "Istanbul"]

def get_weather_data(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric&lang=tr"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def generate_comment(weather_id, temp):
    if 200 <= weather_id < 300: return "Gök gürültülü fırtına var, dikkatli olun! ⚡"
    elif 300 <= weather_id < 600: return "Yağmur yağıyor, şemsiyenizi almayı unutmayın! ☔"
    elif 600 <= weather_id < 700: return "Kar yağıyor! Sıkı giyinin. ❄️"
    elif weather_id == 800: return "Güneşli ve harika bir gün! 😎"
    elif 801 <= weather_id <= 804: return "Hava bulutlu, huzurlu bir gün dileriz. ☁️"
    else: return "Hava durumuna uygun giyinmeyi unutmayın! 🧥"

def main():
    if not all([OPENWEATHER_API_KEY, IG_SESSIONID, INSTAGRAM_GROUP_ID]):
        print("HATA: Eksik çevre değişkeni var.")
        return

    today_str = datetime.now().strftime('%d.%m.%Y')
    message_lines = [f"Günaydın! 🌅 İşte bugünün hava durumu raporu ({today_str}):\n"]

    for city in CITIES:
        try:
            data = get_weather_data(city)
            weather_id = data["weather"][0]["id"]
            desc = data["weather"][0]["description"].capitalize()
            temp = round(data["main"]["temp"])
            comment = generate_comment(weather_id, temp)
            message_lines.append(f"📍 {city}: {desc}, {temp}°C. {comment}\n")
        except Exception as e:
            message_lines.append(f"📍 {city}: Veri alınamadı 😔\n")

    final_message = "\n".join(message_lines)
    
    try:
        cl = Client()
        cl.set_device({"app_version": "330.0.0.46.117", "android_version": 29, "android_release": "10"})
        cl.login_by_sessionid(IG_SESSIONID)
        cl.direct_send(text=final_message, thread_ids=[int(INSTAGRAM_GROUP_ID)])
        print("Mesaj başarıyla gönderildi!")
    except Exception as e:
        print(f"HATA: {e}")

if __name__ == "__main__":
    main()
