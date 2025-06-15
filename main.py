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
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    try:
        text = soup.find("div", class_="NewsHeadline").find_next("td", {"width": "100%"}).text.strip()
        # Example: "Today's boosted creature: Grim Reaper"
        name = text.split(":")[-1].strip()
        return f"🦴 Boosted Creature: **{name}**"
    except:
        return "❌ Could not find boosted creature."

def scrape_boosted_boss():
    url = "https://www.tibia.com/news/?subtopic=bosstiaryboost"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    try:
        text = soup.find("div", class_="NewsHeadline").find_next("td", {"width": "100%"}).text.strip()
        # Example: "Today's boosted boss: The Count of the Core"
        name = text.split(":")[-1].strip()
        return f"👑 Boosted Boss: **{name}**"
    except:
        return "❌ Could not find boosted boss."

if __name__ == "__main__":
    today = datetime.now().strftime("%Y-%m-%d")
    message = f"📅 Tibia Boosts for {today}\n{scrape_boosted_creature()}\n{scrape_boosted_boss()}"
    print(message)
    send_to_discord(message)
