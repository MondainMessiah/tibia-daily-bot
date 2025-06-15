import os
import asyncio
from playwright.async_api import async_playwright
from datetime import datetime
import requests

async def scrape_boosted():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Scrape boosted creature
        await page.goto("https://www.tibia.com/library/?subtopic=boostedcreature")
        await page.wait_for_load_state("networkidle")
        creature_img = await page.locator("img[alt]").first.get_attribute("alt")

        # Scrape boosted boss
        await page.goto("https://www.tibia.com/library/?subtopic=boostablebosses")
        await page.wait_for_load_state("networkidle")
        boss_img = await page.locator("img[alt]").first.get_attribute("alt")

        await browser.close()
        return creature_img, boss_img

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

    creature = creature if creature and "Boosted" not in creature else "Not found"
    boss = boss if boss and "Boosted" not in boss else "Not found"

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
