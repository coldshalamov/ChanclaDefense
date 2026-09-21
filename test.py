import os
import asyncio
from playwright.async_api import async_playwright

async def run(playwright):
    browser = await playwright.chromium.launch(headless=True)
    page = await browser.new_page()
    await page.goto(f"file://{os.path.abspath('index.html')}")

    # Set canvas size properly
    await page.set_viewport_size({"width": 400, "height": 700})

    # The issue is `chanclas` isn't global, it's inside an IIFE.
    # To properly check, we can rely on screenshot visual testing since it's an invisible mechanic,
    # but first let's just make sure it spawns and runs without errors.

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

    # Click play button based on canvas coordinates
    await page.mouse.click(117, 453)

    # Wait for ghost chancla to spawn and be registered
    await page.wait_for_timeout(3000)

    # See what was drawn, should not have crashed
    await page.screenshot(path="screenshot_in_game.png")

    await browser.close()

async def main():
    async with async_playwright() as playwright:
        await run(playwright)

if __name__ == '__main__':
    asyncio.run(main())
