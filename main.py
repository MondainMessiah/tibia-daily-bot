import os, requests
from bs4 import BeautifulSoup
from datetime import datetime

def send_to_discord(msg):
    url = os.getenv("DISCORD_WEBHOOK_URL")
    if not url:
        print("Webhook not set")
        return
    requests.post(url, json={"content": msg})

def scrape_from_statistic():
    url = "https://www.tibia-statistic.com/"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")
    imgs = soup.find_all("img")
    if len(imgs) >= 2:
        return (
            f"🦴 Boosted Creature: **{imgs[0].get('alt','').strip()}**",
            f"👑 Boosted Boss: **{imgs[1].get('alt','').strip()}**"
        )
    return "❌ Couldn't find boosted creature", "❌ Couldn't find boosted boss"

if __name__ == '__main__':
    creature, boss = scrape_from_statistic()
    date = datetime.now().strftime("%Y-%m-%d")
    msg = f"📅 Tibia Boosts for {date}\n{creature}\n{boss}"
    print(msg)
    send_to_discord(msg)
