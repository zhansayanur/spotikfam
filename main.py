import threading
import schedule
import telebot
import requests
from datetime import date, time
from telebot import types
import random

bot = telebot.TeleBot('7169783286:AAEWb_S1zj_dkTrL-MPsGSbcU_QawgeybAc')
price = 7.99
people = 5

def get_usd_to_kzt():
    try:
        url = f"http://api.exchangerate.host/live?access_key=7f2da1a2d27daa31ae571d6af7cac879&source=USD&currencies=KZT&format=1"
        response = requests.get(url)
        data = response.json()

        if not data.get("success"):
            raise ValueError(f"Ошибка от API: {data.get('error', {}).get('info', 'неизвестная ошибка')}")

        return data["quotes"]["USDKZT"]
    except Exception as e:
        print("Ошибка при получении курса:", e)
        return None

@bot.message_handler(commands=['spotify'])
def send_payment_info(message):
    rate = get_usd_to_kzt()
    if not rate:
        bot.send_message(message.chat.id, "⚠️ Не удалось получить курс валют. Попробуйте позже.")
        return

    today = date.today()
    if today.day >= 13:
        target_month = today.month
    else:
        target_month = today.month - 1 if today.month > 1 else 12

    month_names = [
        "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
        "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
    ]
    month_name = month_names[target_month - 1]

    total_kzt = price * rate
    per_person = round(total_kzt / people, 2)

    text = (
        f"*Герлики напоминание об оплате Spotify за {month_name}* 🎧 \n\n"
        f"Общая сумма: *${price}* ≈ *{int(total_kzt)} ₸*\n"
        f"С каждой *~{per_person} ₸* на номер Жансаи Н. (+7 777 734-58-58).\n\n"
        "_Заранее благодарю! 🥰_"
    )

    bot.send_message(message.chat.id, text, parse_mode="Markdown")


@bot.message_handler(commands=['ban'])
def start(message):
    bot.send_message(message.chat.id, 'Ой, как мило. Всего хорошего! Ну, или как получится 😌 Идите нахуй 😇')

@bot.message_handler(commands=['report'])
def start(message):
    bot.send_message(message.chat.id, 'Себя репортни 😇')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton('Spotify', callback_data='payment')
    btn2 = types.InlineKeyboardButton('Прогулка 🌿', callback_data='walk')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, 'Привет! Чего желаете? 🥰 ', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'payment')
def handle_payment_callback(call):
    bot.answer_callback_query(call.id)
    rate = get_usd_to_kzt()
    if not rate:
        bot.send_message(call.message.chat.id, "⚠️ Не удалось получить курс валют. Попробуйте позже.")
        return

    today = date.today()
    if today.day >= 13:
        target_month = today.month
    else:
        target_month = today.month - 1 if today.month > 1 else 12

    month_names = [
        "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
        "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
    ]
    month_name = month_names[target_month - 1]

    total_kzt = price * rate
    per_person = round(total_kzt / people, 2)

    text = (
        f"*Spotify за {month_name}* 🎧 \n\n"
        f"Общая сумма: *${price}* ≈ *{int(total_kzt)} ₸*\n"
        f"С каждой *~{per_person} ₸* на номер Жансаи Н. (+7 777 734-58-58).\n\n"
        "_Заранее благодарю! 🥰_"
    )

    bot.send_message(call.message.chat.id, text, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == 'walk')
def handle_walk_callback(call):
    bot.answer_callback_query(call.id)

    places = [
        "Парк Первого Президента 🌳",
        "Терренкур 🌳",
        "Кок-Тобе/Горы 🏞️",
        "Арбат 🎨",
        "Кафе ☕",
        "Ботанический сад 🌿",
        "Набережная Есентай 🌉",
        "Прогулка на Чимбулак 🚡",
        "Смотровая на Медео 🌌",
        "Кино или кофе на выбор 🎬☕",
        "А не желаете ли пойти в ж... 🥰",
        "Галерея ARTиШОК или выставка 🎭"
    ]

    choice = random.choice(places)
    bot.send_message(call.message.chat.id, f"📍 Предложение для прогулки для настоящих Almighty people:\n\n*{choice}*", parse_mode="Markdown")

def run_scheduler():
    schedule.every().day.at("10:00").do(check_date_and_remind)
    while True:
        schedule.run_pending()

def check_date_and_remind():
    today = date.today()
    if today.day == 13:
        chat_id = -1002171316024 
        send_scheduled_reminder(chat_id)

def send_scheduled_reminder(chat_id):
    rate = get_usd_to_kzt()
    if not rate:
        bot.send_message(chat_id, "⚠️ Не удалось получить курс валют. Попробуйте позже.")
        return

    today = date.today()
    target_month = today.month

    month_names = [
        "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
        "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
    ]
    month_name = month_names[target_month - 1]

    total_kzt = price * rate
    per_person = round(total_kzt / people, 2)

    text = (
        f"*Герлики напоминание об оплате Spotify за {month_name}* 🎧 \n\n"
        f"Общая сумма: *${price}* ≈ *{int(total_kzt)} ₸*\n"
        f"С каждой *~{per_person} ₸* на номер Жансаи Н. (+7 777 734-58-58).\n\n"
        "_Заранее благодарю! 🥰_"
    )

    bot.send_message(chat_id, text, parse_mode="Markdown")

threading.Thread(target=run_scheduler, daemon=True).start()

bot.polling(none_stop=True)