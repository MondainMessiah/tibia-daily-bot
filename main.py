import os, requests
from bs4 import BeautifulSoup
from datetime import datetime

def send_to_discord(msg):
    webhook = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook:
        print("Missing webhook URL")
        return
    requests.post(webhook, json={"content": msg})

def scrape_boosted_creature():
    url = "https://www.tibia.com/library/?subtopic=boostedcreature"
    resp = requests.get(url, headers={"User-Agent":"Mozilla/5.0"})
    soup = BeautifulSoup(resp.text, "html.parser")
    el = soup.find("td", string=lambda t: "Today's Boosted Creature" in t)
    if el:
        return el.find_next_sibling("td").get_text(strip=True)
    return "❌ Creature not found"

def scrape_boosted_boss():
    url = "https://www.tibia.com/library/?subtopic=boostablebosses"
    resp = requests.get(url, headers={"User-Agent":"Mozilla/5.0"})
    soup = BeautifulSoup(resp.text, "html.parser")
    el = soup.find("td", string=lambda t: "Today's boosted boss" in t)
    if el:
        return el.find_next_sibling("td").get_text(strip=True)
    return "❌ Boss not found"

if __name__ == "__main__":
    creature = scrape_boosted_creature()
    boss = scrape_boosted_boss()
    date = datetime.now().strftime("%Y-%m-%d")
    msg = f"📅 Tibia Boosts for {date}\n🦴 Boosted Creature: **{creature}**\n👑 Boosted Boss: **{boss}**"
    print(msg)
    send_to_discord(msg)
