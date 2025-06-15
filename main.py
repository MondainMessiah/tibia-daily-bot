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
        creature = await page.locator("img[alt]").first.get_attribute("alt")
        
        # Scrape boosted boss
        await page.goto("https://www.tibia.com/library/?subtopic=boostablebosses")
        boss = await page.locator("img[alt]").first.get_attribute("alt")
        
        await browser.close()
        return creature, boss

def send_to_discord(msg):
    url = os.getenv("DISCORD_WEBHOOK_URL")
    if not url:
        print("Webhook URL missing")
        return
    requests.post(url, json={"content": msg})

async def main():
    creature, boss = await scrape_boosted()
    date = datetime.now().strftime("%Y-%m-%d")
    msg = f"📅 Tibia Boosts for {date}\n🦴 Boosted Creature: **{creature or 'Not found'}**\n👑 Boosted Boss: **{boss or 'Not found'}**"
    print(msg)
    send_to_discord(msg)

if __name__ == "__main__":
    asyncio.run(main())
