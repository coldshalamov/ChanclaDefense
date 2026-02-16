
from playwright.sync_api import sync_playwright
import time
import os

def verify_shop():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        cwd = os.getcwd()
        page.goto('file://' + cwd + '/index.html')

        # Wait for canvas
        canvas = page.locator('#game')
        canvas.wait_for()

        # Take Title Screenshot
        page.screenshot(path='verification/title_screen_shop_btn.png')
        print("Title screen screenshot taken.")

        # Click Shop Button (coordinates approx x=center, y=460)
        # Canvas size 400x700. Shop button rect: 110, 440, 46, 12.
        # Wait, rect(110, 440, W-220, 46).
        # Center x=200. Y=463.
        print("Entering Shop...")
        page.mouse.click(200, 463)
        time.sleep(0.5)

        # Take Shop Screenshot
        page.screenshot(path='verification/shop_screen.png')
        print("Shop screen screenshot taken.")

        # Cheat Coins via console
        print("Adding coins...")
        page.evaluate("() => { window.game_cheat_coins = 1000; }")
        # Wait, my variables are inside IIFE. I can't access them directly.
        # But localStorage is accessible!
        # Coins are loaded from localStorage in initTitle -> loadStats.
        # If I update localStorage and reload, it might work?
        # Or I can try to click "Buy" and fail, then maybe ...

        # Actually, since it's IIFE, I can't easily cheat variables unless I exposed them.
        # But I implemented save/load stats.
        # So I can set localStorage item and reload page.

        print("Setting localStorage coins...")
        page.evaluate("localStorage.setItem('cb_coins', '1000')")
        page.reload()

        # Wait for reload
        time.sleep(0.5)

        # Go back to Shop
        print("Entering Shop again...")
        page.mouse.click(200, 463)
        time.sleep(0.5)

        page.screenshot(path='verification/shop_screen_rich.png')

        # Buy VapoRub (Item 0). Y = 120 + 0 * (90+15) + 45 = 165.
        # Buy button is at right side.
        # x = 30, w = 400-60 = 340. Button X ~ 30+340-80-10 = 280. Center ~ 320.
        print("Buying VapoRub...")
        page.mouse.click(320, 165)
        time.sleep(0.2)

        page.screenshot(path='verification/shop_screen_bought.png')

        # Exit Shop. Y = 700 - 80 + 25 = 645.
        print("Exiting Shop...")
        page.mouse.click(200, 645)
        time.sleep(0.5)

        # Start Game (Play Button: Y=400)
        print("Starting Game...")
        page.mouse.click(200, 400)
        time.sleep(0.5)

        # Verify Shield (Visual check via screenshot)
        page.screenshot(path='verification/game_start_shield.png')
        print("Game start screenshot taken (should see shield).")

        browser.close()

if __name__ == '__main__':
    verify_shop()
