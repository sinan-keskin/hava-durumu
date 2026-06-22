import os
import requests
from instagrapi import Client
from datetime import datetime

# Çevre değişkenlerinden hassas verileri alıyoruz
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")
INSTAGRAM_GROUP_ID = os.getenv("INSTAGRAM_GROUP_ID")

CITIES = ["Ankara", "Istanbul"]

def get_weather_data(city):
    """OpenWeatherMap API'sinden belirtilen şehrin hava durumu verisini çeker."""
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric&lang=tr"
    response = requests.get(url)
    response.raise_for_status() # HTTP hatası varsa exception fırlatır
    return response.json()

def generate_comment(weather_id, temp):
    """Hava durumu koduna ve sıcaklığa göre özel ve eğlenceli yorumlar üretir."""
    # OpenWeatherMap hava durumu kodlarına göre gruplandırma:
    # 2xx: Fırtına, 3xx: Çisenti, 5xx: Yağmur, 6xx: Kar, 7xx: Atmosferik (Sis vb.), 800: Açık, 80x: Bulutlu
    
    if 200 <= weather_id < 300:
        return "Gök gürültülü fırtına var, dikkatli olun ve gerekmedikçe dışarı çıkmayın! ⚡🌩️"
    elif 300 <= weather_id < 600:
        return "Yağmur yağıyor, şemsiyenizi almadan evden çıkmayın! Islanmanızı istemeyiz. ☔🌧️"
    elif 600 <= weather_id < 700:
        return "Kar yağıyor! Sıkı giyinin, atkı ve eldivenlerinizi unutmayın, kartopu savaşına hazırlıklı olun! ❄️⛄"
    elif weather_id == 800:
        if temp > 25:
            return "Güneş pırıl pırıl ve hava çok sıcak! Güneş kreminizi sürün, güneş gözlüğünüzü ve şapkanızı takmayı unutmayın! 🕶️☀️"
        else:
            return "Hava açık ve harika görünüyor! Temiz havanın ve güneşin tadını çıkarın. ☀️😎"
    elif 801 <= weather_id <= 804:
        return "Hava bugün bulutlu, belki biraz kasvetli olabilir ama gününüzün aydınlık geçmesini dileriz! ☁️⛅"
    else:
        return "Hava durumuna uygun giyinmeyi ve hazırlıklı olmayı unutmayın! 🧥"

def main():
    # 1. Gerekli tüm çevre değişkenlerinin tanımlı olduğundan emin olalım
    if not all([OPENWEATHER_API_KEY, INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD, INSTAGRAM_GROUP_ID]):
        print("HATA: Eksik çevre değişkeni var. Lütfen tüm Secrets (gizli değişkenler) ayarlarını yaptığınızdan emin olun.")
        return

    # 2. Mesaj taslağını hazırlayalım
    today_str = datetime.now().strftime('%d.%m.%Y')
    message_lines = [f"Günaydın! 🌅 İşte bugünün hava durumu raporu ({today_str}):\n"]

    # Her iki şehir için hava durumu verisini çekip mesajı oluşturalım
    for city in CITIES:
        try:
            data = get_weather_data(city)
            weather_id = data["weather"][0]["id"]
            desc = data["weather"][0]["description"].capitalize()
            temp = round(data["main"]["temp"])
            feels_like = round(data["main"]["feels_like"])
            
            comment = generate_comment(weather_id, temp)
            
            city_report = f"📍 {city}:\n"
            city_report += f"Durum: {desc}\n"
            city_report += f"Sıcaklık: {temp}°C (Hissedilen: {feels_like}°C)\n"
            city_report += f"Tavsiye: {comment}\n"
            
            message_lines.append(city_report)
        except Exception as e:
            print(f"HATA: {city} için hava durumu çekilirken bir sorun oluştu: {e}")
            message_lines.append(f"📍 {city}: Hava durumu verisi alınamadı 😔\n")

    message_lines.append("Harika bir gün geçirmeniz dileğiyle! ✨")
    
    # Tüm satırları birleştirerek tek bir metin haline getirelim
    final_message = "\n".join(message_lines)
    print("Oluşturulan Mesaj:\n", final_message)

    # 3. Instagram'a giriş yapıp mesajı gruba gönderelim
    try:
        print("Instagram'a giriş yapılıyor...")
        cl = Client()
        cl.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
        
        print(f"Mesaj {INSTAGRAM_GROUP_ID} ID'li gruba gönderiliyor...")
        # thread_ids parametresi int listesi kabul eder.
        cl.direct_send(text=final_message, thread_ids=[int(INSTAGRAM_GROUP_ID)])
        print("Mesaj başarıyla gönderildi!")
    except Exception as e:
        print(f"HATA: Instagram'a mesaj gönderilirken bir sorun oluştu: {e}")

if __name__ == "__main__":
    main()
