
from playwright.sync_api import sync_playwright
import time
import os

def verify_shop():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        cwd = os.getcwd()
        page.goto('file://' + cwd + '/index.html')

        # Inject coins
        page.evaluate("() => { localStorage.setItem('chancla_bomb_save', JSON.stringify({ coins: 10000, upgrades: { lives: 0, shield: 0, cooldown: 0, luck: 0 }, skins: { gold: false }, bestScore: 0 })); }")
        page.reload()

        # Enter Shop
        # Click on Shop Button (approx coordinates based on previous code: 110, 450)
        # We can use text selector "Shop / Tienda" if it's text, but canvas.
        # Let's click by coordinates.
        # Canvas size 400x700. Shop button is at y=450.
        canvas = page.locator('#game')
        canvas.click(position={'x': 200, 'y': 470})
        time.sleep(0.5)

        # Verify we are in shop (take screenshot)
        page.screenshot(path='verification/shop_initial.png')
        print('Initial Shop screenshot taken.')

        # Buy Lives Level 1 (First item, y=150)
        canvas.click(position={'x': 200, 'y': 185})
        time.sleep(0.2)

        # Buy Luck Level 1 (Fourth item, y=150 + 85*3 = 405)
        canvas.click(position={'x': 200, 'y': 440})
        time.sleep(0.2)

        # Buy Gold Skin (Fifth item, y=150 + 85*4 = 490)
        canvas.click(position={'x': 200, 'y': 525})
        time.sleep(0.2)

        page.screenshot(path='verification/shop_purchased.png')
        print('Purchased Shop screenshot taken.')

        # Return to Title
        # Back button at bottom
        canvas.click(position={'x': 200, 'y': 630})
        time.sleep(0.5)

        # Start Game
        # Play button at y=380
        canvas.click(position={'x': 200, 'y': 400})
        time.sleep(1)

        # Take screenshot of gameplay to see Gold Skin
        page.screenshot(path='verification/gameplay_gold.png')
        print('Gameplay Gold screenshot taken.')

        browser.close()

if __name__ == '__main__':
    verify_shop()
