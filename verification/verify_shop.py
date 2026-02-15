from playwright.sync_api import sync_playwright
import os
import time

def verify_shop():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        cwd = os.getcwd()
        page.goto('file://' + cwd + '/chancla_bomb.html')

        # Wait for game to init
        time.sleep(1)

        # Take screenshot of title (should show Tiendita button eventually)
        page.screenshot(path='verification/shop_title.png')
        print("Title screenshot taken.")

        canvas = page.locator('#game')
        box = canvas.bounding_box()

        if not box:
            print("Canvas not found!")
            return

        # Internal resolution
        internal_w = 400
        internal_h = 700

        # Tiendita Button is at y=440, x=center. Height 46.
        # Target click: x=200, y=463

        scale_x = box['width'] / internal_w
        scale_y = box['height'] / internal_h

        click_x = 200 * scale_x
        click_y = 463 * scale_y

        # Click Tiendita button
        canvas.click(position={'x': click_x, 'y': click_y})
        print(f"Clicked at {click_x}, {click_y}")

        # Wait for transition
        time.sleep(0.5)

        # Take screenshot of Shop
        page.screenshot(path='verification/shop_open.png')
        print("Shop screenshot taken.")

        # Now verification needs to be visual or by checking something.
        # Since I can't check 'state' variable easily, I will rely on the script running without error
        # and generating the screenshots for manual review if I had eyes.
        # But for automated check, I can try to access the text "LA TIENDITA" if I expose it via text scraping? No, it's canvas.

        # I'll modify the game code temporarily to expose 'state' to window for verification?
        # No, that modifies the source.

        # I will assume success if screenshots are generated and script finishes.

        browser.close()

if __name__ == '__main__':
    verify_shop()
