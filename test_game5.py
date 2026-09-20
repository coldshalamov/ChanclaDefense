from playwright.sync_api import sync_playwright
import os
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"file://{os.path.abspath('index.html')}")

        # Start game
        page.click("canvas")
        time.sleep(0.5)

        # Force next chancla to be ghost
        page.evaluate("Math.random = () => 0.04;")
        time.sleep(1.0)

        screenshot_path = "/home/jules/verification/screenshot5.png"
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")
        browser.close()

if __name__ == "__main__":
    run()
