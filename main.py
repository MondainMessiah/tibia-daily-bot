import os
import asyncio
from playwright.async_api import async_playwright
from datetime import datetime
import requests

async def scrape_boosted():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Boosted Creature page
        await page.goto("https://www.tibia.com/library/?subtopic=boostedcreature")
        await page.wait_for_selector("div.BoxContent")
        creature_imgs = await page.locator("div.BoxContent img").all()
        creature_img_alts = [await img.get_attribute("alt") for img in creature_imgs]
        creature_text = await page.locator("div.BoxContent").inner_text()

        # Boosted Boss page
        await page.goto("https://www.tibia.com/library/?subtopic=boostablebosses")
        await page.wait_for_selector("div.BoxContent")
        boss_imgs = await page.locator("div.BoxContent img").all()
        boss_img_alts = [await img.get_attribute("alt") for img in boss_imgs]
        boss_text = await page.locator("div.BoxContent").inner_text()

        await browser.close()
        return (creature_img_alts, creature_text), (boss_img_alts, boss_text)

def send_to_discord(msg):
    webhook = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook:
        print("❌ DISCORD_WEBHOOK_URL environment variable is missing.")
        return
    response = requests.post(webhook, json={"content": msg})
    print("✅ Sent to Discord:", response.status_code)

async def main():
    (creature_img_alts, creature_text), (boss_img_alts, boss_text) = await scrape_boosted()
    date = datetime.now().strftime("%Y-%m-%d")

    message = (
        f"📅 Tibia Boosts for {date}\n\n"
        f"🦴 Creature image alt texts:\n{creature_img_alts}\n\n"
        f"🦴 Creature raw text:\n{creature_text}\n\n"
        f"👑 Boss image alt texts:\n{boss_img_alts}\n\n"
        f"👑 Boss raw text:\n{boss_text}"
    )
    print(message)
    send_to_discord(message)

if __name__ == "__main__":
    asyncio.run(main())
