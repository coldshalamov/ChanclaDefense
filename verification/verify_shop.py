
from playwright.sync_api import sync_playwright
import time
import os

def verify_shop():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the game
        cwd = os.getcwd()
        page.goto('file://' + cwd + '/chancla_bomb.html')
        canvas = page.locator('#game')

        # Wait for load
        time.sleep(1)

        # Take Title Screenshot
        page.screenshot(path='verification/shop_0_title.png')
        print('Title screenshot taken.')

        # Click "Tiendita" button (approx x=200, y=473 based on logic)
        # Button y=450 to 496. Center y=473.
        canvas.click(position={'x': 200, 'y': 473})

        time.sleep(0.5)

        # Take Shop Screenshot
        page.screenshot(path='verification/shop_1_open.png')
        print('Shop screenshot taken.')

        # Click "Back" button (approx x=200, y=653)
        # Button y=630 to 676. Center y=653.
        canvas.click(position={'x': 200, 'y': 653})

        time.sleep(0.5)

        # Take Back Screenshot (should be title)
        page.screenshot(path='verification/shop_2_back.png')
        print('Back to Title screenshot taken.')

        browser.close()

if __name__ == '__main__':
    verify_shop()
