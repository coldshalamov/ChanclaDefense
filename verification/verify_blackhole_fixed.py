import os
import re
import asyncio
from playwright.async_api import async_playwright

async def verify_blackhole():
    html_path = os.path.abspath('index.html')
    temp_path = os.path.abspath('verification/temp_blackhole.html')

    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Force game state and timeElapsed to spawn blackhole quickly
    content = content.replace('let state = STATE.TITLE;', 'let state = STATE.PLAYING;')
    content = content.replace('let timeElapsed = 0;', 'let timeElapsed = 35;')
    # Remove the play button requirement since we forced playing state
    content = content.replace('if (state === STATE.TITLE) {', 'if (false) {')

    with open(temp_path, 'w', encoding='utf-8') as f:
        f.write(content)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(f'file://{temp_path}')

        # Wait a moment for black hole to spawn and fall
        await page.wait_for_timeout(2000)

        os.makedirs('verification/screenshots', exist_ok=True)
        await page.screenshot(path='verification/screenshots/blackhole_falling_fixed.png', full_page=True)
        print("Took falling screenshot")

        # Click canvas to try to slap the black hole
        box = await page.locator('canvas#game').bounding_box()
        if box:
            await page.mouse.click(box['x'] + box['width'] / 2, box['y'] + box['height'] - 100)
            await page.wait_for_timeout(500)
            await page.screenshot(path='verification/screenshots/blackhole_burst_fixed.png', full_page=True)
            print("Took burst screenshot")

        await browser.close()

    if os.path.exists(temp_path):
        os.remove(temp_path)

if __name__ == '__main__':
    asyncio.run(verify_blackhole())
