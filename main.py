import os
import asyncio
from playwright.async_api import async_playwright
from datetime import datetime
import requests

async def scrape_boosted():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # ✅ Scrape boosted creature (from BoxContent text)
        await page.goto("https://www.tibia.com/library/?subtopic=boostedcreature")
        await page.wait_for_selector("div.BoxContent")
        creature_text = await page.locator("div.BoxContent").inner_text()

        # ✅ Scrape boosted boss (from BoxContent text)
        await page.goto("https://www.tibia.com/library/?subtopic=boostablebosses")
        await page.wait_for_selector("div.BoxContent")
        boss_text = await page.locator("div.BoxContent").inner_text()

        await browser.close()
        return creature_text.strip(), boss_text.strip()

def send_to_discord(msg):
    webhook = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook:
        print("❌ DISCORD_WEBHOOK_URL environment variable is missing.")
        return
    response = requests.post(webhook, json={"content": msg})
    print("✅ Sent to Discord:", response.status_code)

async def main():
    creature_text, boss_text = await scrape_boosted()
    date = datetime.now().strftime("%Y-%m-%d")

    # Basic fallback detection
    creature = "Not found" if "no creature" in creature_text.lower() else creature_text.splitlines()[0]
    boss = "Not found" if "no boss" in boss_text.lower() else boss_text.splitlines()[0]

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
