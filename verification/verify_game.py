
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

        # Start game by clicking the Play button
        # The button is at y=380 to 426 on a 700 height canvas.
        # That is roughly 54% to 60% down the canvas.
        # We need to click specifically there.
        canvas = page.locator('#game')
        box = canvas.bounding_box()

        # Click at approximate relative coordinates of the Play button
        # x=center, y=~400/700
        click_x = box['width'] * 0.5
        click_y = box['height'] * (403 / 700)

        page.mouse.click(box['x'] + click_x, box['y'] + click_y)

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
