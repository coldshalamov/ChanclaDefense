import os
import time
from playwright.sync_api import sync_playwright

def verify_slap():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        cwd = os.getcwd()
        file_path = f"file://{cwd}/chancla_bomb.html"
        page.goto(file_path)

        # Wait for canvas
        canvas = page.locator("#game")
        canvas.wait_for()

        # Click the canvas to start game
        print("Clicking canvas...")
        canvas.click()

        # Wait for game to initialize (fade out of title etc)
        # resetGame() sets state = PLAYING immediately.
        # But we want to ensure the next frame catches the input.
        time.sleep(0.5)

        # Trigger Slap
        print("Triggering Slap...")
        page.keyboard.press("Space")

        # Wait to capture the slap effect
        time.sleep(0.05)

        screenshot_path = "verification/slap_verification_2.png"
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

        browser.close()

if __name__ == "__main__":
    verify_slap()
