import os
import asyncio
from playwright.async_api import async_playwright
from datetime import datetime
import requests

async def scrape_boosted():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/115.0.0.0 Safari/537.36"
        ))
        page = await context.new_page()

        # Scrape boosted creature
        await page.goto("https://www.tibia.com/library/?subtopic=boostedcreature")
        await page.wait_for_selector("div.BoxContent")
        await page.wait_for_timeout(4000)  # wait a bit for content to load

        # Try to get image alt attribute first
        creature_img = await page.locator("div.BoxContent img").first
        creature_img_alt = await creature_img.get_attribute("alt") if creature_img else None

        # Fallback: get the first line of the text inside BoxContent
        creature_text = await page.locator("div.BoxContent").inner_text()
        creature_name = creature_img_alt or (creature_text.splitlines()[0] if creature_text else None)

        # Scrape boosted boss
        await page.goto("https://www.tibia.com/library/?subtopic=boostablebosses")
        await page.wait_for_selector("div.BoxContent")
        await page.wait_for_timeout(4000)

        boss_img = await page.locator("div.BoxContent img").first
        boss_img_alt = await boss_img.get_attribute("alt") if boss_img else None

        boss_text = await page.locator("div.BoxContent").inner_text()
        boss_name = boss_img_alt or (boss_text.splitlines()[0] if boss_text else None)

        await browser.close()

        return creature_name.strip() if creature_name else None, boss_name.strip() if boss_name else None

def send_to_discord(msg):
    webhook = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook:
        print("❌ DISCORD_WEBHOOK_URL environment variable not set.")
        return
    response = requests.post(webhook, json={"content": msg})
    print(f"Discord response status: {response.status_code}")

async def main():
    creature, boss = await scrape_boosted()
    date = datetime.now().strftime("%Y-%m-%d")

    if not creature or "no boosted" in creature.lower():
        creature = "No boosted creature found."
    if not boss or "no boosted" in boss.lower():
        boss = "No boosted boss found."

    message = (
        f"📅 Tibia Boosts for {date}\n"
        f"🦴 Boosted Creature: **{creature}**\n"
        f"👑 Boosted Boss: **{boss}**"
    )

    print(message)
    send_to_discord(message)

if __name__ == "__main__":
    asyncio.run(main())
