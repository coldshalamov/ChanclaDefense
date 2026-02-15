from playwright.sync_api import sync_playwright
import time
import os
import json

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        cwd = os.getcwd()
        # Ensure we point to chancla_bomb.html since index.html might not be updated yet
        page.goto(f'file://{cwd}/chancla_bomb.html')

        # Inject coins to test buying
        page.evaluate("() => { localStorage.setItem('cb_coins', '1000'); }")
        page.reload()
        time.sleep(1)

        # 1. Check Title Screen
        page.screenshot(path='verification/shop_1_title.png')
        print("Title screen screenshot taken.")

        box = page.locator('#game').bounding_box()
        scale_x = box['width'] / 400
        scale_y = box['height'] / 700

        # 2. Click Shop Button (Title Screen: y=440 to 480. Center 460)
        shop_btn_x = box['x'] + 200 * scale_x
        shop_btn_y = box['y'] + 460 * scale_y

        page.mouse.click(shop_btn_x, shop_btn_y)
        time.sleep(1)
        page.screenshot(path='verification/shop_2_inside.png')
        print("Shop screen screenshot taken.")

        # 3. Buy VapoRub (Item 1: y starts 120. Button y=135, h=35. Center y=152.5)
        # Button x=300, w=70. Center x=335.
        buy_btn_x = box['x'] + 335 * scale_x
        buy_btn_y = box['y'] + 152.5 * scale_y

        page.mouse.click(buy_btn_x, buy_btn_y)
        time.sleep(0.5)
        page.screenshot(path='verification/shop_3_bought.png')
        print("Bought item screenshot taken.")

        # 4. Check localStorage
        inventory_str = page.evaluate("() => localStorage.getItem('cb_inventory')")
        print(f"Inventory: {inventory_str}")

        inventory = json.loads(inventory_str)

        if inventory.get('vaporub', 0) > 0:
             print("SUCCESS: VapoRub purchased.")
        else:
             print("FAILURE: VapoRub not purchased.")
             exit(1)

        browser.close()

if __name__ == '__main__':
    run()
