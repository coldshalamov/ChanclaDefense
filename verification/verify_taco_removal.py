from playwright.sync_api import sync_playwright
import os
import time

def verify_taco_removal():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 450, 'height': 800})

        cwd = os.getcwd()
        page.goto('file://' + cwd + '/chancla_bomb.html')

        # Click the canvas to start
        page.wait_for_selector("#game")
        page.click("#game")

        # Wait for the game to run for a bit
        time.sleep(3)

        page.screenshot(path="verification/game_after_taco_removal.png")
        print("Screenshot taken: verification/game_after_taco_removal.png")

        browser.close()

if __name__ == '__main__':
    verify_taco_removal()
