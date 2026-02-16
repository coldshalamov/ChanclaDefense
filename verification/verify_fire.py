from playwright.sync_api import sync_playwright
import os
import time

def test_fire_aura():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the test file
        url = "file://" + os.path.abspath("test_fire.html")
        page.goto(url)

        # Wait for canvas
        page.wait_for_selector("canvas#game")

        # Click to start game
        page.click("canvas#game")

        # Wait for a moment for particles to spawn
        time.sleep(2)

        # Take screenshot
        page.screenshot(path="verification/fire_aura.png")
        print("Screenshot taken: verification/fire_aura.png")

        browser.close()

if __name__ == "__main__":
    test_fire_aura()
