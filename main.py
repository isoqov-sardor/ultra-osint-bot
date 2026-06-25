import telebot
import requests
import json
import hashlib
import time
import concurrent.futures
from urllib.parse import quote

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

# ============ BOT BUYRUQLARI ============

@bot.message_handler(commands=['start'])
def boshlash(xabar):
    bot.reply_to(xabar, """
<b>🔍 ULTRA-OSINT BOT</b>

100+ platformada odam qidirish
24/7 ishlaydi | Telefon orqali

<b>📌 Buyruqlar:</b>
/username <i>nick</i> - Username qidirish
/email <i>@mail.com</i> - Email qidirish
/name <i>Ism Fam</i> - Ism-familiya
/phone <i>+998...</i> - Telefon qidirish
/full <i>user email tel</i> - To'liq qidiruv

<b>Misol:</b> /username alisher
    """)

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
    
    try:
        bot.edit_message_text(matn, xabar.chat.id, xabar_id.message_id, disable_web_page_preview=True)
    except:
        bot.send_message(xabar.chat.id, matn, disable_web_page_preview=True)

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
    
    try:
        bot.edit_message_text(matn, xabar.chat.id, xabar_id.message_id, disable_web_page_preview=True)
    except:
        bot.send_message(xabar.chat.id, matn, disable_web_page_preview=True)

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
    
    bot.edit_message_text(matn, xabar.chat.id, xabar_id.message_id, disable_web_page_preview=True)

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
    
    try:
        bot.edit_message_text(matn, xabar.chat.id, xabar_id.message_id, disable_web_page_preview=True)
    except:
        bot.send_message(xabar.chat.id, matn, disable_web_page_preview=True)

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
    
    try:
        bot.edit_message_text(matn, xabar.chat.id, xabar_id.message_id, disable_web_page_preview=True)
    except:
        bot.send_message(xabar.chat.id, matn, disable_web_page_preview=True)

@bot.message_handler(func=lambda m: True)
def avto_qidir(xabar):
    """Har qanday matnni avtomatik qidirish"""
    matn = xabar.text.strip()
    
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

while True:
    try:
        bot.infinity_polling(timeout=30)
    except Exception as x:
        print(f"❌ Xatolik: {x}")
        print("🔄 5 soniyadan keyin qayta ulanadi...")
        time.sleep(5)
