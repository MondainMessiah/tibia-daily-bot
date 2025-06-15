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

        # Boosted Creature
        await page.goto("https://www.tibia.com/library/?subtopic=boostedcreature")
        await page.wait_for_selector("div.BoxContent")
        await page.wait_for_timeout(4000)
        creature_html = await page.locator("div.BoxContent").inner_html()

        # Boosted Boss
        await page.goto("https://www.tibia.com/library/?subtopic=boostablebosses")
        await page.wait_for_selector("div.BoxContent")
        await page.wait_for_timeout(4000)
        boss_html = await page.locator("div.BoxContent").inner_html()

        await browser.close()
        return creature_html, boss_html

def send_to_discord(msg):
    webhook = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook:
        print("❌ DISCORD_WEBHOOK_URL environment variable not set.")
        return
    response = requests.post(webhook, json={"content": msg})
    print(f"Discord response status: {response.status_code}")

async def main():
    creature_html, boss_html = await scrape_boosted()
    date = datetime.now().strftime("%Y-%m-%d")

    message = (
        f"📅 Tibia Boosts for {date}\n\n"
        f"🦴 Boosted Creature HTML:\n```\n{creature_html[:1500]}\n```\n\n"
        f"👑 Boosted Boss HTML:\n```\n{boss_html[:1500]}\n```"
    )

    print(message)
    send_to_discord(message)

if __name__ == "__main__":
    asyncio.run(main())
