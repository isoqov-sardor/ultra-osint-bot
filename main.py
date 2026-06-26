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
    bot.reply_to(xabar, "🤖 ULTRA-OSINT BOT ishga tushdi!\n📌 Buyruqlar uchun /menu ni bosing.")

@bot.message_handler(commands=['username'])
def username_buyruq(xabar):
    # ... username qidiruv kodi ...

@bot.message_handler(commands=['email'])
def email_buyruq(xabar):
    # ... email qidiruv kodi ...

@bot.message_handler(commands=['phone'])
def telefon_buyruq(xabar):
    # ... telefon qidiruv kodi ...

@bot.message_handler(commands=['name'])
def ism_buyruq(xabar):
    # ... ism familiya qidiruv kodi ...

@bot.message_handler(commands=['full'])
def full_buyruq(xabar):
    # ... to‘liq qidiruv kodi ...

# === Yangi menyu handler ===
@bot.message_handler(commands=['menu'])
def menyu(xabar):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    knopka1 = types.KeyboardButton("🔍 Username")
    knopka2 = types.KeyboardButton("📧 Email")
    knopka3 = types.KeyboardButton("📱 Telefon")
    knopka4 = types.KeyboardButton("👤 Ism-Familiya")
    knopka5 = types.KeyboardButton("🧩 To‘liq qidiruv")
    knopka6 = types.KeyboardButton("ℹ️ Yordam")
    markup.add(knopka1, knopka2, knopka3, knopka4, knopka5, knopka6)
    bot.send_message(xabar.chat.id, "📌 Qidiruv turini tanlang:", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def tugma_handler(xabar):
    matn = xabar.text.strip()
    if matn == "🔍 Username":
        bot.reply_to(xabar, "✍️ Username yozing: /username johndoe")
    elif matn == "📧 Email":
        bot.reply_to(xabar, "✍️ Email yozing: /email test@gmail.com")
    elif matn == "📱 Telefon":
        bot.reply_to(xabar, "✍️ Telefon yozing: /phone +998901234567")
    elif matn == "👤 Ism-Familiya":
        bot.reply_to(xabar, "✍️ Ism familiya yozing: /name John Doe")
    elif matn == "🧩 To‘liq qidiruv":
        bot.reply_to(xabar, "✍️ Format: /full username email telefon")
    elif matn == "ℹ️ Yordam":
        bot.reply_to(xabar, """
📖 Yordam menyusi:
/username johndoe – Username qidirish
/email test@gmail.com – Email qidirish
/phone +998901234567 – Telefon qidirish
/name John Doe – Ism-Familiya qidirish
/full johndoe test@gmail.com +998901234567 – To‘liq qidiruv
        """)
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
        time.sleep(5)
