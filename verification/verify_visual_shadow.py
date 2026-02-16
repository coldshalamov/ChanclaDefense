import os
import time
from playwright.sync_api import sync_playwright

def verify_visual_shadow():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load game
        cwd = os.getcwd()
        page.goto('file://' + cwd + '/chancla_bomb.html')

        # Click to start
        canvas = page.locator('#game')
        canvas.click()

        # Wait for chanclas to spawn (approx 1.2s spawn interval)
        print("Waiting for chanclas to spawn...")
        time.sleep(2.5)

        # Take screenshot
        screenshot_path = 'verification/shadow_verification.png'
        page.screenshot(path=screenshot_path)
        print(f"Screenshot taken at {screenshot_path}")

        browser.close()

if __name__ == "__main__":
    verify_visual_shadow()
