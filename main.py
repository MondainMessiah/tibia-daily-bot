import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def send_to_discord(message: str):
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("No Discord webhook URL found.")
        return
    requests.post(webhook_url, json={"content": message})

def scrape_boosted_creature():
    url = "https://www.tibia.com/news/?subtopic=creatureboost"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    img = soup.find("img", alt=True)
    return f"🦴 Boosted Creature: **{img['alt']}**" if img else "No boosted creature found."

def scrape_boosted_boss():
    url = "https://www.tibia.com/news/?subtopic=bosstiaryboost"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    img = soup.find("img", alt=True)
    return f"👑 Boosted Boss: **{img['alt']}**" if img else "No boosted boss found."

if __name__ == "__main__":
    today = datetime.now().strftime("%Y-%m-%d")
    message = f"📅 Tibia Boosts for {today}\n{scrape_boosted_creature()}\n{scrape_boosted_boss()}"
    print(message)
    send_to_discord(message)
