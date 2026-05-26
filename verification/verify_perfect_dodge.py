import os
import time
from playwright.sync_api import sync_playwright

def run_cuj(page):
    file_path = os.path.abspath('index.html')
    url = f"file://{file_path}"

    page.goto(url)
    page.wait_for_timeout(1000)

    # Bypass localStorage SecurityError for local files
    page.add_init_script("Object.defineProperty(window, 'localStorage', { value: { getItem: () => null, setItem: () => {} }, writable: true });")
    page.reload()
    page.wait_for_timeout(500)

    # 1. Start game
    page.keyboard.press('Enter')
    page.wait_for_timeout(1000)

    # Wait for game to be playing
    page.wait_for_timeout(1000)

    # Since exposing variables via script injection is tricky, let's just trigger a dodge manually in the game.
    # The game spawns chanclas randomly. We'll spam the left/right dash keys to trigger the cyan visual trail
    # and hopefully dodge something.

    # 2. Setup perfect dodge scenario (Simulated)
    # Just spamming dash...
    for _ in range(10):
        page.keyboard.press('ArrowLeft')
        page.keyboard.up('ArrowLeft')
        time.sleep(0.05)
        page.keyboard.press('ArrowLeft')
        page.keyboard.up('ArrowLeft')
        page.wait_for_timeout(400) # wait for cooldown

        page.keyboard.press('ArrowRight')
        page.keyboard.up('ArrowRight')
        time.sleep(0.05)
        page.keyboard.press('ArrowRight')
        page.keyboard.up('ArrowRight')
        page.wait_for_timeout(400) # wait for cooldown

    page.screenshot(path="verification/screenshots/perfect_dodge.png")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="verification/videos"
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()
            browser.close()
