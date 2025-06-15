import os
import asyncio
from playwright.async_api import async_playwright
from datetime import datetime
import requests

async def scrape_boosted():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # 🔍 Boosted Creature
        await page.goto("https://www.tibia.com/library/?subtopic=boostedcreature")
        await page.wait_for_selector("div.BoxContent img")
        creature = await page.locator("div.BoxContent img").first.get_attribute("alt")

        # 🔍 Boosted Boss
        await page.goto("https://www.tibia.com/library/?subtopic=boostablebosses")
        await page.wait_for_selector("div.BoxContent img")
        boss = await page.locator("div.BoxContent img").first.get_attribute("alt")

        await browser.close()
        return creature, boss

def send_to_discord(msg):
    webhook = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook:
        print("❌ DISCORD_WEBHOOK_URL environment variable is missing.")
        return
    response = requests.post(webhook, json={"content": msg})
    print("✅ Sent to Discord:", response.status_code)

async def main():
    creature, boss = await scrape_boosted()
    date = datetime.now().strftime("%Y-%m-%d")

    # Handle cases where content is not found or generic
    creature = creature if creature and "boosted creature" not in creature.lower() else "Not found"
    boss = boss if boss and "boosted boss" not in boss.lower() else "Not found"

    message = (
        f"📅 Tibia Boosts for {date}\n"
        f"🦴 Boosted Creature: **{creature}**\n"
        f"👑 Boosted Boss: **{boss}**"
    )

    print("DEBUG creature:", creature)
    print("DEBUG boss:", boss)
    print("Sending to Discord...\n", message)
    send_to_discord(message)

if __name__ == "__main__":
    asyncio.run(main())
