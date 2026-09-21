import os
import asyncio
from playwright.async_api import async_playwright

async def run(playwright):
    browser = await playwright.chromium.launch(headless=True)
    page = await browser.new_page()
    await page.goto(f"file://{os.path.abspath('index.html')}")

    # Set canvas size properly
    await page.set_viewport_size({"width": 400, "height": 700})

    # Send Enter key to start the game directly, bypassing canvas coordinate click issues
    await page.keyboard.press("Enter")

    await page.evaluate("""
        let rngCount = 0;
        Math.random = function() {
            rngCount++;
            if (rngCount >= 5) {
                return 0.1; // trigger ghost which is <0.15
            }
            return 0.99; // bypass others
        };
    """)

    # Wait for ghost chancla to spawn and be registered
    await page.wait_for_timeout(3000)

    # See what was drawn, should not have crashed
    await page.screenshot(path="screenshot_in_game2.png")

    await browser.close()

async def main():
    async with async_playwright() as playwright:
        await run(playwright)

if __name__ == '__main__':
    asyncio.run(main())
