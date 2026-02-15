from playwright.sync_api import sync_playwright
import time
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load game
        cwd = os.getcwd()
        page.goto('file://' + cwd + '/chancla_bomb.html')

        # Wait for load
        time.sleep(1)

        # Take screenshot of title screen with Shop button
        page.screenshot(path='verification/title_screen_with_shop.png')
        print('Title screen captured.')

        # Locate canvas
        canvas = page.locator('#game')
        box = canvas.bounding_box()
        if box:
            # Click "Tiendita" button
            # Button is at x=110, y=440 relative to canvas (400x700)
            # Center x=200, y=460
            click_x = box['x'] + 200
            click_y = box['y'] + 460
            page.mouse.click(click_x, click_y)

            time.sleep(0.5)
            page.screenshot(path='verification/shop_screen.png')
            print('Shop screen captured.')

            # Click "SALIR" button
            # Exit button is at y=630, height=50. Center y=655.
            exit_x = box['x'] + 200
            exit_y = box['y'] + 655
            page.mouse.click(exit_x, exit_y)

            time.sleep(0.5)
            page.screenshot(path='verification/back_to_title.png')
            print('Back to title captured.')

        browser.close()

if __name__ == '__main__':
    run()
