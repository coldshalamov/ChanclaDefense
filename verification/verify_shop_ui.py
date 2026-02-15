
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
        box = canvas.bounding_box()

        # Click Tiendita button on Title Screen
        # y=440 to 486 on 700 height canvas.
        # Center approx 463.
        click_x = box['width'] * 0.5
        click_y = box['height'] * (463 / 700)

        page.mouse.click(box['x'] + click_x, box['y'] + click_y)

        time.sleep(1)
        page.screenshot(path='verification/shop_ui.png')
        print('Shop UI screenshot taken.')

        browser.close()

if __name__ == '__main__':
    verify_shop()
