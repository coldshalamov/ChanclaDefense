from playwright.sync_api import sync_playwright
import time
import os
import json

def verify_shop():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        cwd = os.getcwd()
        page.goto('file://' + cwd + '/chancla_bomb.html')

        # 1. Inject coins via localStorage and reload
        print("Injecting coins via localStorage...")
        page.evaluate("""() => {
            localStorage.setItem('chancla_bomb_save', JSON.stringify({
                coins: 2000,
                upgrades: { lives: 0, shield: 0, cooldown: 0 }
            }));
        }""")
        page.reload()
        time.sleep(1) # Wait for init

        # 2. Open Shop
        print("Opening Shop...")
        box = page.locator('#game').bounding_box()
        if not box:
            print("Canvas not found")
            return

        click_x = box['x'] + (200 / 400) * box['width']
        click_y = box['y'] + (463 / 700) * box['height']

        page.mouse.click(click_x, click_y)
        time.sleep(1) # Wait for transition

        # 3. Verify Shop State (Screenshot)
        page.screenshot(path='verification/shop_screen_actual.png')

        # 4. Buy Lives (First item)
        # y = 160. center = 200, 160 + 60 = 220.
        buy_y = box['y'] + (220 / 700) * box['height']
        page.mouse.click(click_x, buy_y)
        time.sleep(0.5)

        # Verify upgrade via localStorage
        save_data = page.evaluate("() => localStorage.getItem('chancla_bomb_save')")
        data = json.loads(save_data)
        lives_upgrade = data['upgrades'].get('lives', 0)

        print(f"Lives Upgrade Level: {lives_upgrade}")
        if lives_upgrade != 1:
            print("Failed to buy lives upgrade.")
            exit(1)

        print("Shop verification passed!")
        browser.close()

if __name__ == '__main__':
    verify_shop()
