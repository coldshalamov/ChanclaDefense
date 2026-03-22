import os
import time
from playwright.sync_api import sync_playwright

def verify_phone_removed():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Mobile viewport is crucial for the canvas scaling
        context = browser.new_context(viewport={'width': 450, 'height': 800}, has_touch=True, is_mobile=True)
        page = context.new_page()

        file_path = f"file://{os.path.abspath('index.html')}"

        # Open file path directly to avoid content set issues with strict security contexts
        page.goto(file_path)

        # Click play button
        page.mouse.click(200, 400)
        time.sleep(1.0)

        # Take a screenshot to show game running without chisme timer logic
        page.screenshot(path="verification/game_running_without_phone.png")

        browser.close()

if __name__ == "__main__":
    verify_phone_removed()
