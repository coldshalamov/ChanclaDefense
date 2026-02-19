from playwright.sync_api import sync_playwright
import time
import os

def verify_shop():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        cwd = os.getcwd()
        page.goto('file://' + cwd + '/index.html')

        canvas = page.locator('#game')

        # Take a screenshot of Title Screen (to see Shop button)
        time.sleep(0.5)
        page.screenshot(path='verification/title_with_shop.png')
        print('Title screen screenshot taken.')

        # Click Shop Button.
        # Shop button is at Y=460+23 = 483. X=Center.
        # Canvas is 400x700. Click at 200, 483.
        canvas.click(position={'x': 200, 'y': 483})

        time.sleep(0.5)
        page.screenshot(path='verification/shop_screen.png')
        print('Shop screen screenshot taken.')

        # Click Back button. Y=canvas.height - 80 + 25 = 645.
        canvas.click(position={'x': 200, 'y': 645})

        time.sleep(0.5)
        page.screenshot(path='verification/title_after_back.png')
        print('Title after back screenshot taken.')

        browser.close()

if __name__ == '__main__':
    verify_shop()
