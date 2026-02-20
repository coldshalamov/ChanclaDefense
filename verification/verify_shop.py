
from playwright.sync_api import sync_playwright
import time
import os

def verify_shop():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        cwd = os.getcwd()
        page.goto('file://' + cwd + '/chancla_bomb.html')

        canvas = page.locator('#game')

        # Get bounding box
        box = canvas.bounding_box()
        if not box:
            print("Canvas not found")
            return

        # Click Shop Button (Title Screen)
        # Shop button is at Y=440-486 in 700 height. Center 463.
        # 463 / 700 = 0.66
        click_x = box['width'] * 0.5
        click_y = box['height'] * 0.66
        canvas.click(position={'x': click_x, 'y': click_y}, force=True)

        time.sleep(0.5)
        page.screenshot(path='verification/shop_screen.png')
        print('Shop screen screenshot taken.')

        # Click Back Button (Shop Screen)
        # Back button is at Y=620-670. Center 645.
        # 645 / 700 = 0.92
        click_y_back = box['height'] * 0.92
        canvas.click(position={'x': click_x, 'y': click_y_back}, force=True)

        time.sleep(0.5)
        page.screenshot(path='verification/title_screen_return.png')
        print('Returned to title screen screenshot taken.')

        browser.close()

if __name__ == '__main__':
    verify_shop()
