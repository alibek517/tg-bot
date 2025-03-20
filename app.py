<<<<<<< HEAD
import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv
from datetime import datetime, timedelta
import json

# .env fayldan token, guruh ID va admin chat ID ni olish
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID_raw = os.getenv("GROUP_ID")
ADMIN_CHAT_ID_raw = os.getenv("ADMIN_CHAT_ID")

if not TOKEN or not GROUP_ID_raw or not ADMIN_CHAT_ID_raw:
    raise ValueError("BOT_TOKEN, GROUP_ID yoki ADMIN_CHAT_ID aniqlanmadi! .env faylni tekshiring.")

try:
    GROUP_ID = int(GROUP_ID_raw)
    ADMIN_CHAT_ID = int(ADMIN_CHAT_ID_raw)
except ValueError:
    raise ValueError("GROUP_ID va ADMIN_CHAT_ID butun son bo'lishi kerak.")

bot = telebot.TeleBot(TOKEN)

# Foydalanuvchi maʼlumotlarini saqlash: {user_id: {"phone": ..., "order": ..., "driver_request": ..., "start_time": ...}}
users = {}
user_activity = {
    "total_start": 0,
    "start_today": 0,
    "start_yesterday": 0,
    "active_users": 0,  # online foydalanuvchilar
    "last_month_start": 0
}

# ─────────────────────────────────────────────
# /start: Agar kontakt mavjud bo'lsa, yo'nalish tugmalari; aks holda, kontakt so'raladi.
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id

    # Foydalanuvchini boshqarish
    if user_id not in users:
        users[user_id] = {"start_time": datetime.now()}
        user_activity["total_start"] += 1
        user_activity["start_today"] += 1
        
        # O'tgan oydagi foydalanuvchilarni hisoblash
        if datetime.now() - timedelta(days=30) <= users[user_id]["start_time"]:
            user_activity["last_month_start"] += 1
    
    # Kontaktni tekshirish
    if user_id in users and "phone" in users[user_id]:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(KeyboardButton("👤 Shofyor man"))
        markup.add(KeyboardButton("🚖 Toshkentdan Xorazmga taxi karak"), 
                   KeyboardButton("🚖 Xorazmdan Toshkentga taxi karak"))
        bot.send_message(user_id, "📍 Yo'nalishni tanlang yoki shofyor ma'lumotlarini kiritish uchun 'Shofyor man'ni tanlang:", reply_markup=markup)
    else:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(KeyboardButton("📲 Kontakt ulashish", request_contact=True))
        bot.send_message(user_id, "📲 Iltimos, kontakt ma'lumotlaringizni ulashing!", reply_markup=markup)

# ─────────────────────────────────────────────
# Statistikani olish uchun /statistik komandasi
@bot.message_handler(commands=['statistik'])
def statistics(message):
    # Bugungi va kechagi foydalanuvchilarni hisoblash
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    online_users = 0  # Online foydalanuvchilarni hisoblash
    for user_id, data in users.items():
        if (datetime.now() - data["start_time"]).days <= 1:  # online foydalanuvchi
            online_users += 1

    # Kecha va bugun start bosgan foydalanuvchilarni hisoblash
    start_today = 0
    start_yesterday = 0
    for user_id, data in users.items():
        if data["start_time"].date() == today:
            start_today += 1
        elif data["start_time"].date() == yesterday:
            start_yesterday += 1

    # Statistikani yig'ish
    stats = (
        f"📊 Bot Statistikasi:\n\n"
        f"🆔 Jami start bosgan foydalanuvchilar: {user_activity['total_start']}\n"
        f"🔹 Bugun start bosgan foydalanuvchilar: {start_today}\n"
        f"🔹 Kecha start bosgan foydalanuvchilar: {start_yesterday}\n"
        f"🔹 O'tgan bir oyda start bosgan foydalanuvchilar: {user_activity['last_month_start']}\n"
        f"🔹 Online foydalanuvchilar: {online_users}\n"
    )
    
    bot.send_message(message.chat.id, stats)

# ─────────────────────────────────────────────
# Kontaktni qabul qilish
@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    user_id = message.chat.id
    phone = message.contact.phone_number
    users[user_id]["phone"] = phone
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("👤 Shofyor man"))
    markup.add(KeyboardButton("🚖 Toshkentdan Xorazmga taxi karak"), 
               KeyboardButton("🚖 Xorazmdan Toshkentga taxi karak"))
    bot.send_message(user_id, f"✅ Kontakt qabul qilindi: {phone}\n\n📍 Endi yo'nalishni tanlang yoki shofyor ma'lumotlarini kiritish uchun 'Shofyor man'ni tanlang:", reply_markup=markup)

# ─────────────────────────────────────────────
# Botni ishga tushirish
print("🚀 Bot ishga tushdi!")
bot.remove_webhook()  # Webhook'ni olib tashlaymiz
bot.polling(none_stop=True)
=======
import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv
from datetime import datetime, timedelta
import json

# .env fayldan token, guruh ID va admin chat ID ni olish
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID_raw = os.getenv("GROUP_ID")
ADMIN_CHAT_ID_raw = os.getenv("ADMIN_CHAT_ID")

if not TOKEN or not GROUP_ID_raw or not ADMIN_CHAT_ID_raw:
    raise ValueError("BOT_TOKEN, GROUP_ID yoki ADMIN_CHAT_ID aniqlanmadi! .env faylni tekshiring.")

try:
    GROUP_ID = int(GROUP_ID_raw)
    ADMIN_CHAT_ID = int(ADMIN_CHAT_ID_raw)
except ValueError:
    raise ValueError("GROUP_ID va ADMIN_CHAT_ID butun son bo'lishi kerak.")

bot = telebot.TeleBot(TOKEN)

# Foydalanuvchi maʼlumotlarini saqlash: {user_id: {"phone": ..., "order": ..., "driver_request": ..., "start_time": ...}}
users = {}
user_activity = {
    "total_start": 0,
    "start_today": 0,
    "start_yesterday": 0,
    "active_users": 0,  # online foydalanuvchilar
    "last_month_start": 0
}

# ─────────────────────────────────────────────
# /start: Agar kontakt mavjud bo'lsa, yo'nalish tugmalari; aks holda, kontakt so'raladi.
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id

    # Foydalanuvchini boshqarish
    if user_id not in users:
        users[user_id] = {"start_time": datetime.now()}
        user_activity["total_start"] += 1
        user_activity["start_today"] += 1
        
        # O'tgan oydagi foydalanuvchilarni hisoblash
        if datetime.now() - timedelta(days=30) <= users[user_id]["start_time"]:
            user_activity["last_month_start"] += 1
    
    # Kontaktni tekshirish
    if user_id in users and "phone" in users[user_id]:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(KeyboardButton("👤 Shofyor man"))
        markup.add(KeyboardButton("🚖 Toshkentdan Xorazmga taxi karak"), 
                   KeyboardButton("🚖 Xorazmdan Toshkentga taxi karak"))
        bot.send_message(user_id, "📍 Yo'nalishni tanlang yoki shofyor ma'lumotlarini kiritish uchun 'Shofyor man'ni tanlang:", reply_markup=markup)
    else:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(KeyboardButton("📲 Kontakt ulashish", request_contact=True))
        bot.send_message(user_id, "📲 Iltimos, kontakt ma'lumotlaringizni ulashing!", reply_markup=markup)

# ─────────────────────────────────────────────
# Statistikani olish uchun /statistik komandasi
@bot.message_handler(commands=['statistik'])
def statistics(message):
    # Bugungi va kechagi foydalanuvchilarni hisoblash
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    online_users = 0  # Online foydalanuvchilarni hisoblash
    for user_id, data in users.items():
        if (datetime.now() - data["start_time"]).days <= 1:  # online foydalanuvchi
            online_users += 1

    # Kecha va bugun start bosgan foydalanuvchilarni hisoblash
    start_today = 0
    start_yesterday = 0
    for user_id, data in users.items():
        if data["start_time"].date() == today:
            start_today += 1
        elif data["start_time"].date() == yesterday:
            start_yesterday += 1

    # Statistikani yig'ish
    stats = (
        f"📊 Bot Statistikasi:\n\n"
        f"🆔 Jami start bosgan foydalanuvchilar: {user_activity['total_start']}\n"
        f"🔹 Bugun start bosgan foydalanuvchilar: {start_today}\n"
        f"🔹 Kecha start bosgan foydalanuvchilar: {start_yesterday}\n"
        f"🔹 O'tgan bir oyda start bosgan foydalanuvchilar: {user_activity['last_month_start']}\n"
        f"🔹 Online foydalanuvchilar: {online_users}\n"
    )
    
    bot.send_message(message.chat.id, stats)

# ─────────────────────────────────────────────
# Kontaktni qabul qilish
@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    user_id = message.chat.id
    phone = message.contact.phone_number
    users[user_id]["phone"] = phone
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("👤 Shofyor man"))
    markup.add(KeyboardButton("🚖 Toshkentdan Xorazmga taxi karak"), 
               KeyboardButton("🚖 Xorazmdan Toshkentga taxi karak"))
    bot.send_message(user_id, f"✅ Kontakt qabul qilindi: {phone}\n\n📍 Endi yo'nalishni tanlang yoki shofyor ma'lumotlarini kiritish uchun 'Shofyor man'ni tanlang:", reply_markup=markup)

# ─────────────────────────────────────────────
# Botni ishga tushirish
print("🚀 Bot ishga tushdi!")
bot.remove_webhook()  # Webhook'ni olib tashlaymiz
bot.polling(none_stop=True)
>>>>>>> 0789817de5544a2d418f8bca3be656bca89775e9
