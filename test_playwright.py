import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        path = os.path.abspath('index.html')
        await page.goto(f'file://{path}')
        print("Page title:", await page.title())
        await browser.close()

asyncio.run(main())
