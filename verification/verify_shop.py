import os
import re
import time
from playwright.sync_api import sync_playwright

def run_cuj(page):
    with open('index.html', 'r') as f:
        content = f.read()

    # Strip IIFE to expose gameData
    content = re.sub(r'^\s*\(\(\)\s*=>\s*\{\s*', '', content, flags=re.MULTILINE)
    content = re.sub(r'\}\)\(\);\s*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'\blet\s+(gameData|saveGameData|state|STATE|canvas)\b', r'var \1', content)

    temp_path = os.path.abspath('verification/temp_test.html')
    with open(temp_path, 'w') as f:
        f.write(content)

    url = f"file://{temp_path}"

    # Mock localStorage to bypass file:// restrictions
    page.add_init_script("Object.defineProperty(window, 'localStorage', { value: { getItem: () => null, setItem: () => {} }, writable: true });")
    page.goto(url)
    page.wait_for_timeout(500)

    # Click Shop Button (Title Screen)
    # The Play Button is at y:380-426, Shop is at y:440-486, x: 110-290
    page.mouse.click(200, 460)
    page.wait_for_timeout(1000)

    # Give us some money to buy the upgrade
    page.evaluate("window.gameData.coins = 5000; window.saveGameData();")
    # Force a redraw by going back and forth
    page.mouse.click(200, 650) # Click back button
    page.wait_for_timeout(500)
    page.mouse.click(200, 460) # Click shop again
    page.wait_for_timeout(1000)

    # Take screenshot of the shop before purchase
    page.screenshot(path="/home/jules/verification/screenshots/shop_before_purchase.png")

    # Click the new 'Slap Power' upgrade
    # y positions: 120, 215, 310, 405, 500. It's the 5th one, so y=500
    # button is 80px high, so y: 500-580
    page.mouse.click(200, 540)
    page.wait_for_timeout(500)

    page.screenshot(path="/home/jules/verification/screenshots/shop_after_purchase.png")
    page.wait_for_timeout(1000)

if __name__ == "__main__":
    # Ensure directories exist
    os.makedirs("/home/jules/verification/videos", exist_ok=True)
    os.makedirs("/home/jules/verification/screenshots", exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # 400x700 is the canvas size
        context = browser.new_context(
            record_video_dir="/home/jules/verification/videos",
            viewport={'width': 400, 'height': 700}
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()
            browser.close()
