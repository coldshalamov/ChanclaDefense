import os
import sys
from playwright.sync_api import sync_playwright

def verify_pinata_removed():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.on("console", lambda msg: print(f"Browser console: {msg.text}"))
        page.on("pageerror", lambda err: print(f"Browser error: {err}"))

        file_path = os.path.abspath('index.html')
        url = f"file://{file_path}"

        page.add_init_script("Object.defineProperty(window, 'localStorage', { value: { getItem: () => null, setItem: () => {} }, writable: true });")
        page.goto(url)

        # Start game
        page.keyboard.press('Enter')
        page.wait_for_timeout(1000)

        page.screenshot(path="verification/game_after_pinata_removal.png")
        print("Screenshot taken: verification/game_after_pinata_removal.png")
        browser.close()

if __name__ == "__main__":
    verify_pinata_removed()
