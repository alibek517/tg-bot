import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

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

# Foydalanuvchi maʼlumotlarini saqlash: {user_id: {"phone": ..., "order": ...}}
users = {}

# ─────────────────────────────────────────────
# /start: Agar kontakt mavjud bo'lsa, yo'nalish tugmalari; aks holda, kontakt so'raladi.
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    if user_id in users and "phone" in users[user_id]:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
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
    markup.add(KeyboardButton("🚖 Toshkentdan Xorazmga"), KeyboardButton("🚖 Xorazmdan Toshkentga"))
    bot.send_message(user_id, f"✅ Kontakt qabul qilindi: {phone}\n\n📍 Endi yo'nalishni tanlang:", reply_markup=markup)

# ─────────────────────────────────────────────
# Buyurtma qo'yish: Foydalanuvchi yo'nalish tanlaganda, buyurtma yaratiladi va guruhga yuboriladi.
@bot.message_handler(func=lambda message: message.text in ["🚖 Toshkentdan Xorazmga", "🚖 Xorazmdan Toshkentga"])
def handle_order(message):
    user_id = message.chat.id
    if user_id not in users or "phone" not in users[user_id]:
        bot.send_message(user_id, "❌ Iltimos, avval kontaktni ulashing!")
        return
    order_text = message.text
    users[user_id]["order"] = order_text
    # Mijozning username va user ID ni olish
    username = message.from_user.username
    username_disp = f"@{username}" if username else "Noma'lum"
    phone = users[user_id]['phone']
    phone_disp = f"+{phone}" if phone else "Noma'lum"
    # Buyurtma guruhga yuboriladi
    bot.send_message(
        GROUP_ID,
        f"🚖 Yangi buyurtma!\n"
        f"📍 Yo'nalish: {order_text}\n"
        f"🆔 User ID: {user_id}\n"
        f"📞 Kontakt: {phone_disp}\n"
        f"👤 Username: {username_disp}"
    )
    bot.send_message(user_id, "✅ Buyurtmangiz guruhga yuborildi!")

# ─────────────────────────────────────────────
# Fallback: Guruh xabarlarini adminga yubormaslik va foydalanuvchi kontakt ulashmaguncha cheklash
@bot.message_handler(func=lambda message: True)  # Har qanday xabar uchun ishlaydi
def fallback_handler(message):
    user_id = message.chat.id

    # Guruhdagi xabarlarni adminga yubormaslik uchun tekshiramiz
    if message.chat.type in ["group", "supergroup"]:
        return  # Guruhdagi xabarlarni e'tiborsiz qoldiramiz

    # Agar foydalanuvchi kontakt ulashmagan bo‘lsa, undan kontakt so‘raymiz
    if user_id not in users or "phone" not in users[user_id]:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(KeyboardButton("📲 Kontakt ulashish", request_contact=True))
        bot.send_message(user_id, "❌ Iltimos, avval kontaktni ulashing!", reply_markup=markup)
        return

    # Foydalanuvchi ma'lumotlari
    username = message.from_user.username
    username_disp = f"@{username}" if username else "Noma'lum"
    phone = users[user_id]["phone"]
    phone_disp = f"+{phone}" if phone else "Noma'lum"

    # Adminga noma'lum xabarni yuboramiz
    admin_text = (
        f"⚠ *Noma'lum xabar!*\n"
        f"👤 *User:* {username_disp}\n"
        f"📞 *Telefon:* {phone_disp}\n"
        f"🆔 *User ID:* {user_id}\n"
        f"✉ *Xabar:* {message.text}"
    )
    bot.send_message(ADMIN_CHAT_ID, admin_text, parse_mode="Markdown")

# ─────────────────────────────────────────────
# Botni ishga tushirish
print("🚀 Bot ishga tushdi!")
bot.remove_webhook()  # Webhook'ni olib tashlaymiz
bot.polling(none_stop=True)
