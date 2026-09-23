import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        url = f"file://{os.path.abspath('index.html')}"
        print(f"Loading {url} ...")
        await page.goto(url)

        # Start game
        await page.keyboard.press('Space')

        # Give some time for chanclas to spawn
        await page.wait_for_timeout(3000)

        # Override random to force ghost spawns
        await page.evaluate("Math.random = () => 0.14;")

        await page.wait_for_timeout(400)

        # Take a screenshot to verify game is running and ghosts exist
        if not os.path.exists('/home/jules/verification/screenshots'):
            os.makedirs('/home/jules/verification/screenshots')
        await page.screenshot(path='/home/jules/verification/screenshots/game.png')

        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
