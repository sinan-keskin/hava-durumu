import os
import requests
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime

TOKEN = os.getenv("TELEGRAM_TOKEN")
GROUP_ID = os.getenv("TELEGRAM_GROUP_ID")
API_KEY = os.getenv("OPENWEATHER_API_KEY")
bot = telebot.TeleBot(TOKEN)

# --- Orijinal Detaylı Yorum Mantığı ---
def generate_comment(weather_id, temp):
    if 200 <= weather_id < 300: return "Fırtınalı bir hava var, dikkatli olun ve gerekmedikçe dışarı çıkmayın! ⚡🌩️"
    elif 300 <= weather_id < 600: return "Yağmur yağıyor, şemsiyenizi almadan evden çıkmayın! Islanmanızı istemeyiz. ☔🌧️"
    elif 600 <= weather_id < 700: return "Kar yağıyor! Sıkı giyinin, atkı ve eldivenlerinizi unutmayın! ❄️⛄"
    elif 700 <= weather_id < 800: return "Hava biraz puslu veya sisli, görüş mesafesine dikkat! 🌫️"
    elif weather_id == 800:
        if temp > 25: return "Güneş pırıl pırıl ve hava çok sıcak! Güneş kreminizi sürün, güneş gözlüğünüzü takın! 🕶️☀️"
        elif temp < 10: return "Hava güneşli ama soğuk, sıkı giyinmeyi unutmayın! ☀️🥶"
        else: return "Hava açık ve harika görünüyor! Temiz havanın ve güneşin tadını çıkarın. ☀️😎"
    elif 801 <= weather_id <= 804:
        if temp < 10: return "Hava bugün bulutlu ve soğuk, mutlaka kalın giyinmelisin. ☁️🧣"
        else: return "Hava bugün bulutlu, belki biraz kasvetli olabilir ama gününüzün aydınlık geçmesini dileriz! ☁️⛅"
    else: return "Hava durumu biraz değişken, uygun giyinmeyi ve hazırlıklı olmayı unutmayın! 🧥"

# --- Rapor Hazırlama ---
def get_report():
    today_str = datetime.now().strftime('%d.%m.%Y')
    city_data = []
    
    for city in ["Ankara", "Istanbul"]:
        try:
            data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=tr").json()
            city_data.append({
                "name": city,
                "desc": data["weather"][0]["description"].capitalize(),
                "temp": round(data["main"]["temp"]),
                "comment": generate_comment(data["weather"][0]["id"], round(data["main"]["temp"]))
            })
        except:
            city_data.append({"name": city, "desc": "Veri alınamadı", "temp": None, "comment": None})

    # Gruplama
    grouped = {}
    for item in city_data:
        comment = item["comment"]
        if comment not in grouped: grouped[comment] = []
        grouped[comment].append(item)

    # Modern Rapor Oluşturma
    message = f"🌅 *GÜNLÜK HAVA RAPORU* | {today_str}\n━━━━━━━━━━━━━━━━━━━━━━\n"
    for comment, items in grouped.items():
        city_names = ", ".join([i["name"] for i in items])
        message += f"📍 *{city_names.upper()}*\n"
        for i in items:
            if i["temp"] is not None:
                message += f"   • {i['desc']} | *{i['temp']}°C*\n"
            else:
                message += f"   • {i['name']}: Veri alınamadı\n"
        message += f"\n💡 *Tavsiye:* {comment}\n━━━━━━━━━━━━━━━━━━━━━━\n"
    return message

# --- Menü ve Butonlar ---
@bot.message_handler(commands=['s'])
def start(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🌤️ Hava Durumu Raporu", callback_data="weather"))
    markup.add(InlineKeyboardButton("🎮 Oyun", url="https://secrets.sinankeskin.com.tr/"))
    bot.send_message(message.chat.id, "Merhaba! Ne yapmak istersin?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "weather")
def weather_callback(call):
    bot.edit_message_text(get_report(), call.message.chat.id, call.message.message_id, parse_mode="Markdown")

if __name__ == "__main__":
    if os.getenv("GITHUB_ACTIONS"):
        bot.send_message(GROUP_ID, get_report(), parse_mode="Markdown")
    else:
        bot.infinity_polling()
