from tibiapy import fetch_boosted_creature_and_boss
from datetime import datetime
import pytz
import requests
import os

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

def main():
    data = fetch_boosted_creature_and_boss()
    now_london = datetime.now(pytz.timezone("Europe/London")).strftime("%Y-%m-%d %H:%M")

    content = (
        f"📅 **{data.date.strftime('%Y-%m-%d')}**\n"
        f"🧟 **Boosted Creature:** {data.creature.name}\n"
        f"👑 **Boosted Boss:** {data.boss.name}\n"
        f"🕘 Sent at: {now_london} 🇬🇧"
    )

    requests.post(WEBHOOK_URL, json={
        "content": content,
        "username": "Tibia Boost Bot",
        "avatar_url": "https://static.tibia.com/images/global/header/tibiacom_logo.png"
    })

if __name__ == "__main__":
    main()
