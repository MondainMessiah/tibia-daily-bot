import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def send_to_discord(message):
    url = os.getenv("DISCORD_WEBHOOK_URL")
    if not url:
        print("Missing webhook URL")
        return
    requests.post(url, json={"content": message})

def get_boosted_data():
    url = "https://tibia.fandom.com/wiki/Main_Page"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")

    try:
        creature_section = soup.find("a", title="Boosted Creature").find_next("a")
        creature = creature_section["title"]
    except:
        creature = "❌ Creature not found"

    try:
        boss_section = soup.find("a", title="Boosted Boss").find_next("a")
        boss = boss_section["title"]
    except:
        boss = "❌ Boss not found"

    return creature, boss

if __name__ == "__main__":
    creature, boss = get_boosted_data()
    date = datetime.now().strftime("%Y-%m-%d")
    message = f"📅 Tibia Boosts for {date}\n🦴 Boosted Creature: **{creature}**\n👑 Boosted Boss: **{boss}**"
    print(message)
    send_to_discord(message)
