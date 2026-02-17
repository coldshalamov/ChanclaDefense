from playwright.sync_api import sync_playwright
import time
import os

def verify_shop():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Emulate mobile device to match game viewport
        context = browser.new_context(viewport={'width': 420, 'height': 700})
        page = context.new_page()
        cwd = os.getcwd()
        page.goto(f'file://{cwd}/index.html')

        # Wait for title screen
        time.sleep(1)
        page.screenshot(path='verification/title_before_shop.png')

        # Click "Tiendita" button
        # Assuming button will be placed at y=450, centered
        page.mouse.click(210, 460)
        time.sleep(0.5)

        # Take screenshot of shop
        page.screenshot(path='verification/shop_open.png')
        print("Shop opened screenshot taken.")

        # Click Back button
        # Assuming back button will be placed at y=600
        page.mouse.click(210, 610)
        time.sleep(0.5)

        # Verify back to title
        page.screenshot(path='verification/title_after_shop.png')
        print("Shop closed screenshot taken.")

        browser.close()

if __name__ == '__main__':
    verify_shop()
