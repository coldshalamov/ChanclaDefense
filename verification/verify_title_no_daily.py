import os
import time
from playwright.sync_api import sync_playwright

def verify_title():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 450, 'height': 800})
        page = context.new_page()

        file_path = f"file://{os.path.abspath('index.html')}"
        page.goto(file_path)

        # Wait a moment to ensure rendering is complete
        time.sleep(1.0)

        # Take screenshot of the title screen
        screenshot_path = "verification/title_no_daily.png"
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

        browser.close()

if __name__ == "__main__":
    verify_title()
