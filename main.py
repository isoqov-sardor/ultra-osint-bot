import telebot
import requests
import json
import hashlib
import time
import concurrent.futures
from urllib.parse import quote
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ============ TOKEN ============
BOT_TOKEN = "8974671080:AAEyBQ4c31JlNP-tvnj0BxtQHl87PBj73JE"  # <-- BU YERGA TOKENINGIZNI YOZING

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

# ============ PLATFORMALAR ============
PLATFORMS = {
    "Instagram": "https://www.instagram.com/{}/",
    "Telegram": "https://t.me/{}",
    "Twitter (X)": "https://twitter.com/{}",
    "TikTok": "https://www.tiktok.com/@{}",
    "Facebook": "https://www.facebook.com/{}/",
    "LinkedIn": "https://www.linkedin.com/in/{}/",
    "YouTube": "https://www.youtube.com/@{}",
    "Reddit": "https://www.reddit.com/user/{}/",
    "GitHub": "https://github.com/{}",
    "Pinterest": "https://www.pinterest.com/{}/",
    "Twitch": "https://www.twitch.tv/{}",
    "Snapchat": "https://www.snapchat.com/add/{}",
    "Tumblr": "https://{}.tumblr.com",
    "VK": "https://vk.com/{}",
    "OK": "https://ok.ru/{}",
    "Discord": "https://discord.com/users/{}",
    "Medium": "https://medium.com/@{}",
    "Dev.to": "https://dev.to/{}",
    "SoundCloud": "https://soundcloud.com/{}",
    "Spotify": "https://open.spotify.com/user/{}",
    "Behance": "https://www.behance.net/{}",
    "Steam": "https://steamcommunity.com/id/{}/",
    "Roblox": "https://www.roblox.com/user.aspx?username={}",
    "Patreon": "https://www.patreon.com/{}",
    "Ko-Fi": "https://ko-fi.com/{}",
    "BuyMeACoffee": "https://www.buymeacoffee.com/{}",
    "DeviantArt": "https://{}.deviantart.com",
    "Keybase": "https://keybase.io/{}",
    "About.me": "https://about.me/{}",
    "AngelList": "https://angel.co/u/{}",
    "Pastebin": "https://pastebin.com/u/{}",
    "Replit": "https://repl.it/@{}",
    "WordPress": "https://{}.wordpress.com",
    "Blogger": "https://{}.blogspot.com",
    "LeetCode": "https://leetcode.com/{}/",
    "Kaggle": "https://www.kaggle.com/{}",
    "TryHackMe": "https://tryhackme.com/p/{}",
    "HackerOne": "https://hackerone.com/{}",
    "Codewars": "https://www.codewars.com/users/{}",
    "Duolingo": "https://duolingo.com/profile/{}",
    "Goodreads": "https://www.goodreads.com/{}",
    "LastFM": "https://www.last.fm/user/{}",
    "Linktree": "https://linktr.ee/{}",
    "Steemit": "https://steemit.com/@{}",
    "HackerNews": "https://news.ycombinator.com/user?id={}",
    "Codecademy": "https://www.codecademy.com/profiles/{}",
    "Signal": "https://signal.me/{}",
    "Wattpad": "https://www.wattpad.com/user/{}",
    "AskFM": "https://ask.fm/{}",
    "Flickr": "https://www.flickr.com/people/{}/",
    "Bandcamp": "https://bandcamp.com/{}",
    "Vimeo": "https://vimeo.com/{}",
    "GitLab": "https://gitlab.com/{}",
    "Bitbucket": "https://bitbucket.org/{}/",
    "ProductHunt": "https://www.producthunt.com/@{}",
    "Dribbble": "https://dribbble.com/{}",
    "Scribd": "https://www.scribd.com/{}",
    "Unsplash": "https://unsplash.com/@{}",
    "VSCO": "https://vsco.co/{}/gallery",
    "Yelp": "https://www.yelp.com/user_details?userid={}",
    "Zomato": "https://www.zomato.com/{}",
    "Teletype": "https://teletype.in/@{}",
    "Xing": "https://www.xing.com/profile/{}",
    "Issuu": "https://issuu.com/{}",
    "IMDb": "https://www.imdb.com/user/ur{}/",
    "Fandom": "https://www.fandom.com/u/{}",
    "Newgrounds": "https://newgrounds.com/{}",
    "Meetup": "https://www.meetup.com/members/{}/",
    "NPM": "https://www.npmjs.com/~{}",
    "Quizlet": "https://quizlet.com/{}",
    "Quora": "https://www.quora.com/profile/{}",
    "Trakt": "https://trakt.tv/users/{}",
    "Venmo": "https://venmo.com/{}",
    "Viber": "https://viber.com/{}",
    "MyAnimeList": "https://myanimelist.net/profile/{}",
    "Pixabay": "https://pixabay.com/users/{}/",
    "Sketchfab": "https://sketchfab.com/{}",
    "500px": "https://500px.com/{}",
    "DailyMotion": "https://www.dailymotion.com/{}",
    "Letterboxd": "https://letterboxd.com/{}/",
    "Academia": "https://independent.academia.edu/{}",
    "ResearchGate": "https://www.researchgate.net/profile/{}",
    "SourceForge": "https://sourceforge.net/u/{}/profile/",
    "Slideshare": "https://www.slideshare.net/{}",
    "Periscope": "https://www.periscope.tv/{}",
}

session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0'})

def create_menu_keyboard():
    # ============ MENU BUTTON (Telegram bot menyusi) ============
from telebot.types import BotCommand

def set_menu_buttons():
    """Telegram bot menyusiga tugmalarni o'rnatish"""
    commands = [
        BotCommand("start", "🚀 Botni ishga tushirish"),
        BotCommand("menu", "📋 Asosiy menyuni ochish"),
        BotCommand("username", "🔍 Username orqali qidirish"),
        BotCommand("email", "📧 Email orqali qidirish"),
        BotCommand("phone", "📱 Telefon orqali qidirish"),
        BotCommand("name", "👤 Ism familiya orqali qidirish"),
        BotCommand("full", "🔎 To'liq qidiruv (user+email+tel)"),
        BotCommand("tgid", "🆔 Telegram ID yoki @username"),
        BotCommand("forward", "📡 Forward xabarni tahlil qilish"),
        BotCommand("help", "❓ Yordam"),
    ]
    
    try:
        bot.set_my_commands(commands)
        print("✅ Menu tugmalari o'rnatildi!")
        return True
    except Exception as e:
        print(f"❌ Menu tugmalarini o'rnatishda xatolik: {e}")
        return False

# ============ HELP BUYRUQ ============
@bot.message_handler(commands=['help'])
def help_buyruq(xabar):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("🔙 Orqaga", callback_data="menu_back"))
    bot.reply_to(xabar, """
<b>🤖 ULTRA-OSINT BOT - YORDAM</b>

<b>🔍 Username qidirish:</b>
• /username <i>nick</i> - 100+ platformada qidirish
• /tgid @<i>username</i> - Telegram profili

<b>📧 Email qidirish:</b>
• /email <i>user@mail.com</i> - Email orqali

<b>📱 Telefon qidirish:</b>
• /phone <i>+998901234567</i> - Telefon orqali

<b>👤 Ism-Familiya:</b>
• /name <i>Ism Fam</i> - Ism familiya

<b>📡 Forward tahlil:</b>
• Xabarni botga forward qiling

<b>🔎 To'liq qidiruv:</b>
• /full <i>user email tel</i>

⚡ Bot 85+ platformani bir vaqtda tekshiradi
    """, reply_markup=keyboard)

# Menu tugmalarini o'rnatish
set_menu_buttons()
    """Asosiy menyu tugmalari"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("🔍 Username", callback_data="menu_username")
    btn2 = InlineKeyboardButton("📧 Email", callback_data="menu_email")
    btn3 = InlineKeyboardButton("📱 Telefon", callback_data="menu_phone")
    btn4 = InlineKeyboardButton("👤 Ism/Familiya", callback_data="menu_name")
    btn5 = InlineKeyboardButton("🔎 To'liq qidiruv", callback_data="menu_full")
    btn6 = InlineKeyboardButton("🕵️ Telegram ID", callback_data="menu_tgid")
    btn7 = InlineKeyboardButton("📡 Forward tahlil", callback_data="menu_forward")
    btn8 = InlineKeyboardButton("ℹ️ Yordam", callback_data="menu_help")
    keyboard.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8)
    return keyboard

def create_action_keyboard(qidirilgan, qiymat):
    """Qidiruv natijasidan keyin ko'rsatiladigan tugmalar"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("🔄 Qayta qidirish", callback_data=f"req_{qidirilgan}_{qiymat}"),
        InlineKeyboardButton("📋 Asosiy menyu", callback_data="menu_back")
    )
    keyboard.add(
        InlineKeyboardButton("📥 JSON yuklab olish", callback_data=f"json_{qidirilgan}_{qiymat[:20]}"),
        InlineKeyboardButton("📊 Hisobot", callback_data=f"report_{qidirilgan}_{qiymat[:20]}")
    )
    return keyboard

def qidir(username):
    """Asosiy qidiruv funksiyasi"""
    topilgan = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        vazifalar = {}
        for nom, url_shablon in PLATFORMS.items():
            vazifalar[executor.submit(tekshir, nom, url_shablon, username)] = nom
        
        for vazifa in concurrent.futures.as_completed(vazifalar):
            natija = vazifa.result()
            if natija:
                topilgan.append(natija)
    
    return topilgan

def tekshir(nom, url_shablon, username):
    """Bitta platformani tekshirish"""
    try:
        url = url_shablon.format(quote(username))
        javob = session.get(url, timeout=5, allow_redirects=True)
        if javob.status_code == 200:
            return (nom, url)
    except:
        pass
    return None

def tekshir_telegram_id(user_id):
    """Telegram ID bo'yicha ma'lumot (faqat ochiq ma'lumotlar)"""
    natijalar = []
    try:
        # Telegram ochiq API - faqat username dan foydalaniladi
        url = f"https://t.me/{user_id}"
        javob = session.get(url, timeout=5, allow_redirects=True)
        if javob.status_code == 200:
            natijalar.append(("Telegram", url))
    except:
        pass
    return natijalar

# ============ BOT BUYRUQLARI ============

@bot.message_handler(commands=['start'])
def boshlash(xabar):
    keyboard = create_menu_keyboard()
    bot.reply_to(xabar, """
<b>🔍 ULTRA-OSINT BOT</b>

100+ platformada odam qidirish
24/7 ishlaydi

<b>📌 Quyidagi tugmalar orqali buyruq berishingiz mumkin:</b>
    """, reply_markup=keyboard)

@bot.message_handler(commands=['menu'])
def menu_buyruq(xabar):
    keyboard = create_menu_keyboard()
    bot.reply_to(xabar, "<b>📋 ASOSIY MENYU</b>\nKerakli bo'limni tanlang:", reply_markup=keyboard)

@bot.message_handler(commands=['username'])
def username_buyruq(xabar):
    try:
        username = xabar.text.split(maxsplit=1)[1].strip()
    except:
        bot.reply_to(xabar, "❌ Username yozing!\nMisol: /username johndoe")
        return
    
    xabar_id = bot.reply_to(xabar, f"🔍 Qidirilmoqda: @{username}...")
    
    natijalar = qidir(username)
    
    if natijalar:
        matn = f"<b>✅ @{username} topildi! ({len(natijalar)} ta)</b>\n\n"
        for i, (nom, url) in enumerate(natijalar[:20], 1):
            matn += f"{i}. <b>{nom}</b>\n   {url}\n"
        if len(natijalar) > 20:
            matn += f"\n...va yana {len(natijalar)-20} ta platforma"
    else:
        matn = f"❌ @{username} uchun hech narsa topilmadi"
    
    keyboard = create_action_keyboard("username", username)
    
    try:
        bot.edit_message_text(matn, xabar.chat.id, xabar_id.message_id, 
                            disable_web_page_preview=True, reply_markup=keyboard)
    except:
        bot.send_message(xabar.chat.id, matn, disable_web_page_preview=True, reply_markup=keyboard)

@bot.message_handler(commands=['email'])
def email_buyruq(xabar):
    try:
        email = xabar.text.split(maxsplit=1)[1].strip()
    except:
        bot.reply_to(xabar, "❌ Email yozing!\nMisol: /email john@gmail.com")
        return
    
    if '@' not in email:
        bot.reply_to(xabar, "❌ Noto'g'ri email formati!")
        return
    
    xabar_id = bot.reply_to(xabar, f"🔍 Email tekshirilmoqda: {email}")
    
    username = email.split('@')[0]
    matn = f"<b>📧 {email}</b>\n\n"
    
    # Gravatar tekshirish
    hash_kod = hashlib.md5(email.lower().encode()).hexdigest()
    try:
        r = requests.get(f"https://www.gravatar.com/avatar/{hash_kod}?d=404", timeout=5)
        if r.status_code == 200:
            matn += f"🖼 Gravatar profili mavjud\n\n"
    except:
        pass
    
    matn += f"🔍 @{username} bo'yicha qidiruv:\n\n"
    
    try:
        bot.edit_message_text(matn, xabar.chat.id, xabar_id.message_id)
    except:
        pass
    
    natijalar = qidir(username)
    
    if natijalar:
        for nom, url in natijalar[:15]:
            matn += f"• <b>{nom}</b>\n   {url}\n"
        if len(natijalar) > 15:
            matn += f"\n+{len(natijalar)-15} ta ko'proq"
    else:
        matn += "❌ Hech narsa topilmadi"
    
    keyboard = create_action_keyboard("email", email)
    
    try:
        bot.edit_message_text(matn, xabar.chat.id, xabar_id.message_id, 
                            disable_web_page_preview=True, reply_markup=keyboard)
    except:
        bot.send_message(xabar.chat.id, matn, disable_web_page_preview=True, reply_markup=keyboard)

@bot.message_handler(commands=['phone'])
def telefon_buyruq(xabar):
    try:
        telefon = xabar.text.split(maxsplit=1)[1].strip()
    except:
        bot.reply_to(xabar, "❌ Telefon yozing!\nMisol: /phone +998901234567")
        return
    
    xabar_id = bot.reply_to(xabar, f"🔍 Tekshirilmoqda: {telefon}")
    
    toza = telefon.replace("+","").replace(" ","").replace("-","")
    matn = f"<b>📱 {telefon}</b>\n\n"
    
    platformalar = {
        "WhatsApp": f"https://wa.me/{toza}",
        "Telegram": f"https://t.me/{toza}",
        "Viber": f"https://viber.com/{toza}",
        "Signal": f"https://signal.me/{toza}",
    }
    
    for nom, url in platformalar.items():
        try:
            r = session.get(url, timeout=5)
            if r.status_code == 200:
                matn += f"✅ <b>{nom}</b>\n   {url}\n"
        except:
            pass
    
    keyboard = create_action_keyboard("phone", telefon)
    bot.edit_message_text(matn, xabar.chat.id, xabar_id.message_id, 
                         disable_web_page_preview=True, reply_markup=keyboard)

@bot.message_handler(commands=['name'])
def ism_buyruq(xabar):
    try:
        args = xabar.text.split(maxsplit=1)[1].strip().split()
        ism, familiya = args[0], args[1]
    except:
        bot.reply_to(xabar, "❌ Ism familiya yozing!\nMisol: /name John Doe")
        return
    
    xabar_id = bot.reply_to(xabar, f"🔍 Qidirilmoqda: {ism} {familiya}")
    
    variantlar = [
        f"{ism}.{familiya}", f"{ism}{familiya}", f"{ism}_{familiya}",
        f"{ism}{familiya[0]}", f"{ism[0]}{familiya}", f"{familiya}.{ism}",
        f"{familiya}{ism}", ism.lower(), familiya.lower(),
        f"{ism.lower()}.{familiya.lower()}",
        f"{ism.lower()}{familiya.lower()}"
    ]
    
    barchasi = {}
    for v in variantlar:
        natijalar = qidir(v.lower())
        for nom, url in natijalar:
            if nom not in barchasi:
                barchasi[nom] = url
    
    matn = f"<b>👤 {ism} {familiya}</b>\n<b>✅ {len(barchasi)} ta profil</b>\n\n"
    
    for nom, url in list(barchasi.items())[:15]:
        matn += f"• <b>{nom}</b>\n   {url}\n"
    
    if len(barchasi) > 15:
        matn += f"\n+{len(barchasi)-15} ta ko'proq"
    
    if not barchasi:
        matn = f"❌ {ism} {familiya} topilmadi"
    
    keyboard = create_action_keyboard("name", f"{ism}_{familiya}")
    
    try:
        bot.edit_message_text(matn, xabar.chat.id, xabar_id.message_id, 
                            disable_web_page_preview=True, reply_markup=keyboard)
    except:
        bot.send_message(xabar.chat.id, matn, disable_web_page_preview=True, reply_markup=keyboard)

@bot.message_handler(commands=['full'])
def full_buyruq(xabar):
    try:
        qismlar = xabar.text.split(maxsplit=1)[1].strip().split()
        username, email, telefon = qismlar[0], qismlar[1], qismlar[2]
    except:
        bot.reply_to(xabar, "❌ Format: /full username email telefon\nMisol: /full johndoe john@gmail.com +998901234567")
        return
    
    xabar_id = bot.reply_to(xabar, "🔍 TO'LIQ QIDIRUV BOSHLANDI...\nBu bir necha daqiqa olishi mumkin")
    
    u_natija = qidir(username)
    
    email_user = email.split('@')[0]
    e_natija = qidir(email_user)
    
    toza = telefon.replace("+","").replace(" ","").replace("-","")
    p_natija = []
    for nom, url in {"WhatsApp": f"https://wa.me/{toza}", "Telegram": f"https://t.me/{toza}"}.items():
        try:
            r = session.get(url, timeout=5)
            if r.status_code == 200:
                p_natija.append((nom, url))
        except:
            pass
    
    barcha = {}
    for n, u in u_natija + e_natija:
        barcha[n] = u
    
    matn = f"<b>🔍 TO'LIQ QIDIRUV YAKUNLANDI</b>\n\n"
    matn += f"👤 @{username}: <b>{len(u_natija)} ta</b>\n"
    matn += f"📧 {email}: <b>{len(e_natija)} ta</b>\n"
    matn += f"📱 {telefon}: <b>{len(p_natija)} ta</b>\n"
    matn += f"\n📊 Jami: <b>{len(barcha)} ta noyob profil</b>\n\n"
    
    for nom, url in list(barcha.items())[:15]:
        matn += f"• <b>{nom}</b>\n   {url}\n"
    
    if len(barcha) > 15:
        matn += f"\n+{len(barcha)-15} ta ko'proq"
    
    keyboard = create_action_keyboard("full", username)
    
    try:
        bot.edit_message_text(matn, xabar.chat.id, xabar_id.message_id, 
                            disable_web_page_preview=True, reply_markup=keyboard)
    except:
        bot.send_message(xabar.chat.id, matn, disable_web_page_preview=True, reply_markup=keyboard)

# ============ YANGI FUNKSIYALAR ============

@bot.message_handler(commands=['tgid'])
def tgid_buyruq(xabar):
    """Telegram ID yoki @username orqali qidirish"""
    try:
        qiymat = xabar.text.split(maxsplit=1)[1].strip()
    except:
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("🔙 Asosiy menyu", callback_data="menu_back"))
        bot.reply_to(xabar, "❌ Telegram username yoki ID yozing!\nMisol: /tgid @username yoki /tgid 123456789", 
                    reply_markup=keyboard)
        return
    
    xabar_id = bot.reply_to(xabar, f"🔍 Tekshirilmoqda: {qiymat}")
    
    qiymat = qiymat.replace("@", "").strip()
    natijalar = tekshir_telegram_id(qiymat)
    
    matn = f"<b>📡 Telegram ma'lumot: {qiymat}</b>\n\n"
    
    # Telegram orqali qidirish - faqat ochiq ma'lumotlar
    if qiymat.isdigit():
        matn += f"🆔 ID: {qiymat}\n"
        matn += "⚠️ Telegram ID orqali foydalanuvchi ma'lumotlarini olish \n"
        matn += "   cheklangan. Bot guruhda bo'lsa, foydalanuvchini \n"
        matn += "   guruh orqali ko'rish mumkin.\n\n"
    else:
        matn += f"👤 @{qiymat}\n"
        matn += f"🔗 https://t.me/{qiymat}\n\n"
    
    matn += "💡 <b>Forward xabarlar orqali tahlil qilish:</b>\n"
    matn += "Foydalanuvchining xabarini botga forward qiling -> /forward\n\n"
    
    matn += f"🌐 Platformalardan qidirish:\n"
    natijalar = qidir(qiymat)
    if natijalar:
        for nom, url in natijalar[:10]:
            matn += f"• <b>{nom}</b>\n   {url}\n"
    else:
        matn += "❌ Boshqa platformalarda topilmadi\n"
    
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("🔍 Qayta qidirish", callback_data=f"req_tgid_{qiymat}"),
        InlineKeyboardButton("📋 Asosiy menyu", callback_data="menu_back")
    )
    
    try:
        bot.edit_message_text(matn, xabar.chat.id, xabar_id.message_id, 
                            disable_web_page_preview=True, reply_markup=keyboard)
    except:
        bot.send_message(xabar.chat.id, matn, disable_web_page_preview=True, reply_markup=keyboard)

@bot.message_handler(commands=['forward'])
def forward_buyruq(xabar):
    """Forward qilingan xabarni tahlil qilish"""
    bot.reply_to(xabar, """<b>📡 Forward xabar tahlili</b>

Forward qilingan xabarni menga yuboring, men undan ma'lumot olishga harakat qilaman.

<b>Telegram forward xabarlardan olinadigan ma'lumotlar:</b>
• Foydalanuvchi IDsi (forward sender ID)
• Foydalanuvchi username (agar ochiq bo'lsa)
• Xabar kelgan kanal/guruh nomi

<b>Ishlatish:</b>
1. Biror foydalanuvchi yozgan xabarni bosing
2. "Forward" (ulashish) tugmasini bosing
3. Shu botga forward qiling

Yoki /tgid @username buyrug'i bilan username orqali qidiring.
    """)

@bot.message_handler(func=lambda m: m.forward_date is not None)
def forward_qabul(xabar):
    """Forward qilingan xabarni qabul qilish va tahlil qilish"""
    matn = "<b>📡 Forward xabar tahlili</b>\n\n"
    
    # Forward kelgan foydalanuvchi haqida ma'lumot
    if xabar.forward_from:
        f_user = xabar.forward_from
        matn += f"👤 <b>Foydalanuvchi ma'lumotlari:</b>\n"
        matn += f"   ID: <code>{f_user.id}</code>\n"
        if f_user.username:
            matn += f"   Username: @{f_user.username}\n"
            matn += f"   Link: https://t.me/{f_user.username}\n"
        if f_user.first_name:
            matn += f"   Ism: {f_user.first_name}\n"
        if f_user.last_name:
            matn += f"   Familiya: {f_user.last_name}\n"
        
        matn += f"\n🔍 <b>Username bo'yicha qidiruv:</b>\n"
        if f_user.username:
            natijalar = qidir(f_user.username)
            if natijalar:
                for nom, url in natijalar[:10]:
                    matn += f"• <b>{nom}</b>\n   {url}\n"
            else:
                matn += "❌ Topilmadi\n"
    
    # Forward kelgan kanal/guruh haqida
    elif xabar.forward_from_chat:
        chat = xabar.forward_from_chat
        matn += f"📢 <b>Kanal/Guruh ma'lumotlari:</b>\n"
        matn += f"   ID: <code>{chat.id}</code>\n"
        matn += f"   Nomi: {chat.title}\n"
        if chat.username:
            matn += f"   Username: @{chat.username}\n"
        matn += f"   Turi: {chat.type}\n"
    
    # Forward sender name (maxfiy bo'lsa)
    elif xabar.forward_sender_name:
        matn += f"👤 <b>Yuboruvchi (maxfiy):</b>\n"
        matn += f"   Nomi: {xabar.forward_sender_name}\n"
        matn += f"   ⚠️ To'liq ma'lumot maxfiylik tufayli ko'rinmaydi\n"
    
    else:
        matn += "❌ Forward xabardan ma'lumot olish imkoni yo'q\n"
        matn += "Bu foydalanuvchi maxfiylik sozlamalarini cheklagan bo'lishi mumkin\n"
    
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("🔍 Qayta qidirish", callback_data="menu_forward"),
        InlineKeyboardButton("📋 Asosiy menyu", callback_data="menu_back")
    )
    
    bot.reply_to(xabar, matn, reply_markup=keyboard)

# ============ CALLBACK HANDLER ============

@bot.callback_query_handler(func=lambda call: True)
def callback_ishla(call):
    """Tugmalar bosilganda ishlaydi"""
    chat_id = call.message.chat.id
    msg_id = call.message.message_id
    
    if call.data == "menu_back":
        keyboard = create_menu_keyboard()
        bot.edit_message_text("<b>📋 ASOSIY MENYU</b>\nKerakli bo'limni tanlang:", 
                            chat_id, msg_id, reply_markup=keyboard)
    
    elif call.data == "menu_help":
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("🔙 Orqaga", callback_data="menu_back"))
        bot.edit_message_text("""
<b>🤖 ULTRA-OSINT BOT - YORDAM</b>

<b>🔍 Username qidirish:</b>
• /username <i>nick</i> - 100+ platformada qidirish
• /tgid @<i>username</i> - Telegram profili

<b>📧 Email qidirish:</b>
• /email <i>user@mail.com</i> - Email orqali

<b>📱 Telefon qidirish:</b>
• /phone <i>+998901234567</i> - Telefon orqali

<b>👤 Ism-Familiya:</b>
• /name <i>Ism Fam</i> - Ism familiya

<b>📡 Forward tahlil:</b>
• Xabarni botga forward qiling

<b>🔎 To'liq qidiruv:</b>
• /full <i>user email tel</i>

⚡ Bot 85+ platformani bir vaqtda tekshiradi
        """, chat_id, msg_id, reply_markup=keyboard)
    
    elif call.data == "menu_username":
        bot.edit_message_text("📝 Username yozing (masalan: alisher):", chat_id, msg_id)
        bot.register_next_step_handler(call.message, lambda m: username_buyruq(m))
    
    elif call.data == "menu_email":
        bot.edit_message_text("📝 Email yozing (masalan: user@gmail.com):", chat_id, msg_id)
        bot.register_next_step_handler(call.message, lambda m: email_buyruq(m))
    
    elif call.data == "menu_phone":
        bot.edit_message_text("📝 Telefon yozing (masalan: +998901234567):", chat_id, msg_id)
        bot.register_next_step_handler(call.message, lambda m: telefon_buyruq(m))
    
    elif call.data == "menu_name":
        bot.edit_message_text("📝 Ism va familiya yozing (masalan: John Doe):", chat_id, msg_id)
        bot.register_next_step_handler(call.message, lambda m: ism_buyruq(m))
    
    elif call.data == "menu_full":
        bot.edit_message_text("📝 Format: username email telefon\nMisol: johndoe john@gmail.com +998901234567", chat_id, msg_id)
        bot.register_next_step_handler(call.message, lambda m: full_buyruq(m))
    
    elif call.data == "menu_tgid":
        bot.edit_message_text("📝 Telegram ID yoki @username yozing:", chat_id, msg_id)
        bot.register_next_step_handler(call.message, lambda m: tgid_buyruq(m))
    
    elif call.data == "menu_forward":
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("🔙 Orqaga", callback_data="menu_back"))
        bot.edit_message_text("""<b>📡 Forward xabar tahlili</b>

Botga biror foydalanuvchi yoki kanaldan forward qilingan xabarni yuboring.

Menda mavjud imkoniyatlar:
✅ Forward qilgan foydalanuvchi ID, username, ismi
✅ Kanal/guruh ID va nomi
✅ Username bo'yicha boshqa platformalardan qidirish

⚠️ Cheklovlar:
• Agar foydalanuvchi "Forward xabarlarni ulashishni cheklash"ni yoqgan bo'lsa, faqat ismi ko'rinadi
• Foydalanuvchining qaysi guruhlarda ekanligini ko'rib bo'lmaydi (Telegram maxfiylik siyosati)
• Kimlar bilan yozishganini ko'rib bo'lmaydi
        """, chat_id, msg_id, reply_markup=keyboard)
    
    elif call.data.startswith("req_"):
        # Qayta qidirish
        _, turi, qiymat = call.data.split("_", 2)
        bot.edit_message_text(f"🔄 Qayta qidirilmoqda: {qiymat}...", chat_id, msg_id)
        
        if turi == "username":
            username_buyruq(call.message)
        elif turi == "email":
            email_buyruq(call.message)
        elif turi == "phone":
            telefon_buyruq(call.message)
        elif turi == "name":
            ism_buyruq(call.message)
        elif turi == "full":
            full_buyruq(call.message)
        elif turi == "tgid":
            tgid_buyruq(call.message)
    
    elif call.data.startswith("json_"):
        bot.answer_callback_query(call.id, "📥 JSON funksiyasi tez orada qo'shiladi", show_alert=True)
    
    elif call.data.startswith("report_"):
        bot.answer_callback_query(call.id, "📊 Hisobot funksiyasi tez orada qo'shiladi", show_alert=True)
    
    bot.answer_callback_query(call.id)

@bot.message_handler(func=lambda m: True)
def avto_qidir(xabar):
    """Har qanday matnni avtomatik qidirish"""
    matn = xabar.text.strip()
    
    if matn.startswith('/'):
        return
    
    if '@' in matn and '.' in matn:
        email_buyruq(xabar)
    elif matn.startswith('+'):
        telefon_buyruq(xabar)
    else:
        username_buyruq(xabar)

# ============ ISHGA TUSHIRISH ============
print("🤖 ULTRA-OSINT Bot ishga tushdi!")
print(f"📌 Bot: @{bot.get_me().username}")
print(f"📊 Platformalar: {len(PLATFORMS)} ta")
print("✅ Tugmalar bilan menyu faollashtirildi")
print("✅ Forward xabarlarni tahlil qilish faollashtirildi")

while True:
    try:
        bot.infinity_polling(timeout=30)
    except Exception as x:
        print(f"❌ Xatolik: {x}")
        print("🔄 5 soniyadan keyin qayta ulanadi...")
        time.sleep(5)
