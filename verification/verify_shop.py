import os
import sys
from playwright.sync_api import sync_playwright

def run_verification():
    print("Starting Shop Verification...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the game
        file_url = f"file://{os.path.abspath('index.html')}"
        page.goto(file_url)
        print("Game loaded.")
        page.wait_for_timeout(1000)

        # Click Tiendita button (Y=480 approx in Title)
        # My code says 450-496. Center 473.
        print("Clicking Shop Button...")
        page.mouse.click(200, 473)
        page.wait_for_timeout(1000)

        # Screenshot Shop
        page.screenshot(path="verification/shop_screen.png")
        print("Shop screenshot saved.")

        # Click Back (Y=canvas.height - 50 = 650)
        print("Clicking Back...")
        page.mouse.click(200, 650)
        page.wait_for_timeout(500)

        # Click Start (Y=400 approx)
        print("Clicking Start...")
        page.mouse.click(200, 400)
        page.wait_for_timeout(2000) # Wait for game to run a bit

        # Screenshot Game
        page.screenshot(path="verification/game_running_check.png")
        print("Game screenshot saved.")

        browser.close()
        print("Verification complete.")

if __name__ == "__main__":
    run_verification()
