import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def send_to_discord(message):
    webhook = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook:
        print("No webhook found.")
        return
    requests.post(webhook, json={"content": message})

def scrape_boosted_creature():
    url = "https://www.tibia.com/library/?subtopic=boostedcreature"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    img = soup.find("img", {"alt": True})
    if img and "Boosted Creature" not in img["alt"]:
        return img["alt"]
    return "No boosted creature found."

def scrape_boosted_boss():
    url = "https://www.tibia.com/library/?subtopic=boostablebosses"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    img = soup.find("img", {"alt": True})
    if img and "Boosted Boss" not in img["alt"]:
        return img["alt"]
    return "No boosted boss found."

if __name__ == "__main__":
    creature = scrape_boosted_creature()
    boss = scrape_boosted_boss()
    date = datetime.now().strftime("%Y-%m-%d")
    message = f"📅 Tibia Boosts for {date}\n🦴 Boosted Creature: **{creature}**\n👑 Boosted Boss: **{boss}**"
    print(message)
    send_to_discord(message)
