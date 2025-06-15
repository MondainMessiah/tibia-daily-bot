import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def send_to_discord(msg):
    webhook = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook:
        print("Webhook URL missing")
        return
    requests.post(webhook, json={"content": msg})

def scrape_boosts():
    url = "https://www.tibia-statistic.com/"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    imgs = soup.find_all("img")
    if len(imgs) < 2:
        return "❌ No boosted creature found", "❌ No boosted boss found"

    creature = imgs[0].get("alt", "").strip()
    boss = imgs[1].get("alt", "").strip()
    return f"🦴 Boosted Creature: **{creature}**", f"👑 Boosted Boss: **{boss}**"

if __name__ == "__main__":
    creature, boss = scrape_boosts()
    date = datetime.now().strftime("%Y-%m-%d")
    msg = f"📅 Tibia Boosts for {date}\n{creature}\n{boss}"
    print(msg)
    send_to_discord(msg)
