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

        # Force next chancla to be trick (RNG = 0.10)
        # Bomb < 0.08, Golden < 0.05, Trick < 0.10
        # For ghost we used 0.04.

        browser.close()

if __name__ == "__main__":
    run()
