import instaloader
import requests
import time
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

USERNAME = os.getenv("USERNAME")

INSTAGRAM_LOGIN = os.getenv("INSTAGRAM_LOGIN")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text
    })

L = instaloader.Instaloader()

L.login(INSTAGRAM_LOGIN, INSTAGRAM_PASSWORD)

send_message(f"✅ Бот запущен\n📌 Отслеживается: {USERNAME}")

old_followers = set()

while True:
    try:
        profile = instaloader.Profile.from_username(
            L.context,
            USERNAME
        )

        followers = set()

        for follower in profile.get_followers():
            followers.add(follower.username)

        if not old_followers:
            old_followers = followers
            send_message("📥 База подписчиков сохранена")

        else:
            new_followers = followers - old_followers
            lost_followers = old_followers - followers

            for user in new_followers:
                send_message(f"➕ Подписался: @{user}")

            for user in lost_followers:
                send_message(f"➖ Отписался: @{user}")

            old_followers = followers

        time.sleep(300)

    except Exception as e:
        send_message(f"❌ Ошибка:\n{e}")
        time.sleep(60)
