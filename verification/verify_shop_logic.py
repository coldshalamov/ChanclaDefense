from playwright.sync_api import sync_playwright
import json
import time
import os

def verify_shop():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        cwd = os.getcwd()
        url = 'file://' + cwd + '/chancla_bomb.html'

        print(f"Loading {url}")
        page.goto(url)

        # 1. Setup stats with coins
        stats = {
            "bestScore": 100,
            "coins": 1000,
            "inventory": {},
            "totalSlaps": 50
        }
        page.evaluate(f"localStorage.setItem('cb_stats', '{json.dumps(stats)}');")
        page.reload()

        # Get canvas bounding box for scaling
        box = page.locator('#game').bounding_box()
        print(f"Canvas Box: {box}")

        scale_x = box['width'] / 400
        scale_y = box['height'] / 700

        def click_canvas(x, y):
            # x, y are internal coordinates
            # Playwright click position is relative to element
            # We need to account for the difference between internal resolution (400x700) and visual size
            target_x = x * scale_x
            target_y = y * scale_y
            print(f"Clicking at internal ({x}, {y}) -> visual ({target_x}, {target_y})")
            page.locator('#game').click(position={'x': target_x, 'y': target_y})


        # 2. Enter Shop
        print("Entering Shop...")
        click_canvas(200, 473) # Tiendita button center is 450 + 23 = 473
        time.sleep(0.5)
        page.screenshot(path='verification/shop_with_coins.png')

        # 3. Buy VapoRub (Price 150)
        # Item 1 (index 0) y: 120 + 0 * (80 + 10) = 120.
        # Button y = 120 + 20 = 140.
        # Button x = 400 - 110 = 290.
        # Button w = 80, h = 40.
        # Click center: 290 + 40 = 330, 140 + 20 = 160.
        print("Buying VapoRub...")
        click_canvas(330, 160)
        time.sleep(0.2)

        # 4. Verify LocalStorage
        saved_stats_str = page.evaluate("localStorage.getItem('cb_stats')")
        saved_stats = json.loads(saved_stats_str)

        print(f"Stats after purchase: {saved_stats}")

        if saved_stats['coins'] == 850 and saved_stats['inventory'].get('vaporub') == True:
            print("Purchase verification PASSED.")
        else:
            print("Purchase verification FAILED.")
            print(f"Expected coins 850, got {saved_stats['coins']}")
            print(f"Expected vaporub in inventory, got {saved_stats['inventory']}")

        browser.close()

if __name__ == '__main__':
    verify_shop()
