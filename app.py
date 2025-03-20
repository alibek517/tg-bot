import os
import telebot
from dotenv import load_dotenv
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# .env fayldan token va ID'larni yuklash
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID", 0))
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", 0))

# Token tekshirish
if not TOKEN or not GROUP_ID or not ADMIN_CHAT_ID:
    raise ValueError("BOT_TOKEN, GROUP_ID yoki ADMIN_CHAT_ID topilmadi! .env faylni tekshiring.")

bot = telebot.TeleBot(TOKEN)
users = {}  # Foydalanuvchilar ma'lumotlari saqlanadi

# ─────────────────────────────────────────────
# /start buyrug'i
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    if user_id in users and "phone" in users[user_id]:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(KeyboardButton("🧑‍✈️ Shafyorman"))  # Faqat kontaktdan keyin chiqadi
        markup.add(KeyboardButton("🚖 Toshkentdan Xorazmga"), KeyboardButton("🚖 Xorazmdan Toshkentga"))
        bot.send_message(user_id, "📍 Yo'nalishni tanlang:", reply_markup=markup)
    else:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(KeyboardButton("📲 Kontakt ulashish", request_contact=True))
        bot.send_message(user_id, "📲 Iltimos, kontakt ma'lumotlaringizni ulashing!", reply_markup=markup)

# ─────────────────────────────────────────────
# Kontaktni qabul qilish
@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    user_id = message.chat.id
    phone = message.contact.phone_number
    users[user_id] = {"phone": phone}

    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("🧑‍✈️ Shafyorman"))  # Endi tugma chiqadi
    markup.add(KeyboardButton("🚖 Toshkentdan Xorazmga"), KeyboardButton("🚖 Xorazmdan Toshkentga"))
    bot.send_message(user_id, f"✅ Kontakt qabul qilindi: {phone}\n\n📍 Endi yo'nalishni tanlang:", reply_markup=markup)

# ─────────────────────────────────────────────
# Buyurtma berish
@bot.message_handler(func=lambda message: message.text in ["🚖 Toshkentdan Xorazmga", "🚖 Xorazmdan Toshkentga"])
def handle_order(message):
    user_id = message.chat.id
    if user_id not in users or "phone" not in users[user_id]:
        bot.send_message(user_id, "❌ Iltimos, avval kontaktni ulashing!")
        return
    order_text = message.text
    users[user_id]["order"] = order_text

    username = message.from_user.username
    username_disp = f"@{username}" if username else "Noma'lum"
    phone = users[user_id]['phone']

    # Buyurtmani guruhga yuborish
    bot.send_message(
        GROUP_ID,
        f"🚖 Yangi buyurtma!\n"
        f"📍 Yo'nalish: {order_text}\n"
        f"🆔 User ID: {user_id}\n"
        f"📞 Kontakt: +{phone}\n"
        f"👤 Username: {username_disp}"
    )
    bot.send_message(user_id, "✅ Buyurtmangiz guruhga yuborildi!")

# ─────────────────────────────────────────────
# Haydovchilar e'loni
@bot.message_handler(func=lambda message: message.text == "🛠 Shafyorman")
def shafyor_handler(message):
    user_id = message.chat.id
    bot.send_message(user_id, "🚗 Haydovchi e'loningizni kiriting:")
    bot.register_next_step_handler(message, save_shafyor)

def save_shafyor(message):
    user_id = message.chat.id
    elon_text = message.text

    username = message.from_user.username
    username_disp = f"@{username}" if username else "Noma'lum"
    phone = users.get(user_id, {}).get("phone", "Noma'lum")

    # Adminga xabar yuborish
    bot.send_message(
        ADMIN_CHAT_ID,
        f"🚗 Yangi haydovchi e'loni!\n"
        f"🆔 User ID: {user_id}\n"
        f"📞 Telefon: +{phone}\n"
        f"👤 Username: {username_disp}\n"
        f"📝 E'lon: {elon_text}"
    )
    bot.send_message(user_id, "✅ E'loningiz adminga yuborildi!")

# ─────────────────────────────────────────────
# /statistik buyrug'i
@bot.message_handler(commands=['statistik'])
def statistik(message):
    total_users = len(users)
    bot.send_message(message.chat.id, f"📊 Bot foydalanuvchilari soni: {total_users} ta")

# ─────────────────────────────────────────────
# Tushunarsiz xabarlar adminga yuboriladi
@bot.message_handler(func=lambda message: message.text not in ["/start", "/statistik", "🚖 Toshkentdan Xorazmga", "🚖 Xorazmdan Toshkentga", "🛠 Shafyorman"])
def fallback_handler(message):
    user_id = message.chat.id
    username = message.from_user.username
    username_disp = f"@{username}" if username else "Noma'lum"
    phone = users.get(user_id, {}).get("phone", "Noma'lum")

    admin_text = (f"⚠ Noma'lum xabar:\n"
                  f"User ID: {user_id}\n"
                  f"Username: {username_disp}\n"
                  f"Telefon: +{phone}\n"
                  f"Matn: {message.text}")
    bot.send_message(ADMIN_CHAT_ID, admin_text)

# ─────────────────────────────────────────────
# Botni ishga tushirish
print("🚀 Bot ishga tushdi!")
bot.remove_webhook()  # Webhook'ni olib tashlash
bot.polling(none_stop=True)
