
from playwright.sync_api import sync_playwright
import time
import os

def verify_expressions():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the game from the file directly using absolute path
        cwd = os.getcwd()
        page.goto('file://' + cwd + '/chancla_bomb.html')

        # Start game by clicking Play button (approx y=400 on 400x700 canvas)
        # We need to click relative to the bounding box.
        # Ideally we click the Play button area.
        canvas = page.locator('#game')

        # Get bounding box to calculate relative click
        box = canvas.bounding_box()
        if box:
            # Play button is at 380-426 in 700 height.
            # 403 / 700 = 0.575
            click_x = box['width'] * 0.5
            click_y = box['height'] * 0.575
            canvas.click(position={'x': click_x, 'y': click_y})
        else:
            canvas.click() # Fallback

        # Wait a bit for game to start
        time.sleep(1)

        # Take a screenshot of normal state
        page.screenshot(path='verification/normal.png')
        print('Normal state screenshot taken.')

        # Trigger Slap
        page.keyboard.press('Space')

        # Wait a tiny bit for the next frame render (approx 50ms)
        time.sleep(0.05)
        page.screenshot(path='verification/slap.png')
        print('Slap state screenshot taken.')

        browser.close()

if __name__ == '__main__':
    verify_expressions()
