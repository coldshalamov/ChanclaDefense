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

        # Wait for Title
        time.sleep(1)
        page.screenshot(path='verification/shop_test_title.png')

        # Click Shop Button
        # Shop Button: y >= 440 && y <= 486
        # Center Y approx 463
        canvas = page.locator('#game')
        canvas.click(position={'x': 200, 'y': 463})
        time.sleep(1)

        # Verify Shop State (screenshot)
        page.screenshot(path='verification/shop_test_opened.png')
        print("Shop opened screenshot taken.")

        # Click Back Button
        # Back Button: y >= 630 (canvas.height - 70)
        # Center Y approx 653
        canvas.click(position={'x': 200, 'y': 653})
        time.sleep(1)

        # Verify Title State (screenshot)
        page.screenshot(path='verification/shop_test_back.png')
        print("Back to title screenshot taken.")

        browser.close()

if __name__ == '__main__':
    verify_shop()
