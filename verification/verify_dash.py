import os
import time
from playwright.sync_api import sync_playwright

def run_cuj(page):
    # Get absolute path to index.html
    html_path = os.path.abspath('index.html')

    # Load game, bypassing local storage security errors with page.goto
    page.goto(f"file://{html_path}")
    page.wait_for_timeout(1000)

    # Click Jugar to start game
    page.keyboard.press('Enter')
    page.wait_for_timeout(1000)

    # Double tap right arrow quickly to dash
    page.keyboard.press('ArrowRight')
    page.wait_for_timeout(50)
    page.keyboard.press('ArrowRight')

    # Wait briefly to let the dash trail render
    page.wait_for_timeout(100)

    # Take screenshot of the dash trail
    page.screenshot(path="verification/screenshots/dash_verify.png")
    page.wait_for_timeout(1000)

if __name__ == "__main__":
    os.makedirs("verification/screenshots", exist_ok=True)
    os.makedirs("verification/videos", exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="verification/videos",
            viewport={'width': 400, 'height': 700}
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()
            browser.close()
