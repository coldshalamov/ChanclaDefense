
from playwright.sync_api import sync_playwright
import time
import os

def verify_game_index():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the game from the file directly using absolute path
        cwd = os.getcwd()
        page.goto('file://' + cwd + '/index.html')

        # Start game by clicking (simulate touch/click)
        canvas = page.locator('#game')
        canvas.click(position={'x': 200, 'y': 400})

        # Wait a bit for game to start
        time.sleep(1)

        # Take a screenshot of normal state
        page.screenshot(path='verification/index_normal.png')
        print('Normal state screenshot taken.')

        # Trigger Slap
        page.keyboard.press('Space')

        # Wait a tiny bit for the next frame render (approx 50ms)
        time.sleep(0.05)
        page.screenshot(path='verification/index_slap.png')
        print('Slap state screenshot taken.')

        browser.close()

if __name__ == '__main__':
    verify_game_index()
