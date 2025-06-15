import os
import asyncio
from playwright.async_api import async_playwright
from datetime import datetime
import requests

async def scrape_boosted():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Boosted Creature
        await page.goto("https://www.tibia.com/library/?subtopic=boostedcreature")
        await page.wait_for_selector("div.BoxContent")
        creature_img_alt = await page.locator("div.BoxContent img").first.get_attribute("alt")
        creature_text = await page.locator("div.BoxContent").inner_text()
        creature = creature_img_alt or creature_text.splitlines()[0]

        # Boosted Boss
        await page.goto("https://www.tibia.com/library/?subtopic=boostablebosses")
        await page.wait_for_selector("div.BoxContent")
        boss_img_alt = await page.locator("div.BoxContent img").first.get_attribute("alt")
        boss_text = await page.locator("div.BoxContent").inner_text()
        boss = boss_img_alt or boss_text.splitlines()[0]

        await browser.close()
        return creature.strip(), boss.strip()

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

    # Fallback if the text contains no boosted info
    if not creature or "boosted" in creature.lower():
        creature = "No boosted creature found."
    if not boss or "boosted" in boss.lower():
        boss = "No boosted boss found."

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
