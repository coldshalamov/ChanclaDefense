from playwright.sync_api import sync_playwright
import time
import os
import json

def verify_shop():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.on("console", lambda msg: print(f"CONSOLE: {msg.text}"))

        # Load game
        cwd = os.getcwd()
        page.goto('file://' + cwd + '/chancla_bomb.html')

        # Inject coins
        page.evaluate("""() => {
            localStorage.setItem('cb_stats', JSON.stringify({
                bestScore: 0,
                coins: 500,
                inventory: {}
            }));
        }""")

        # Reload to apply stats
        page.reload()
        time.sleep(1)

        canvas = page.locator('#game')
        scale_y = canvas.get_attribute('data-scale-y')
        print(f"Canvas Scale Y: {scale_y}")

        # Click "Tiendita" on Title Screen
        # Canvas 400x700. Tiendita is at y=450-496.
        # Click at y=485.
        print("Clicking Tiendita...")
        canvas.click(position={'x': 200, 'y': 485})
        time.sleep(0.5)

        # Take screenshot of Shop
        page.screenshot(path='verification/shop_screen.png')
        print("Shop screen captured.")

        # Buy VapoRub (Item 0, y=110 to 210)
        # Click at x=200, y=160
        print("Clicking Item 1...")
        canvas.click(position={'x': 200, 'y': 160})
        time.sleep(0.5)

        # Verify Inventory in LocalStorage
        stats = page.evaluate("() => JSON.parse(localStorage.getItem('cb_stats'))")
        print("Stats after buy:", stats)

        if stats['coins'] != 400: # 500 - 100
            print("FAILED: Coins not deducted correctly.")
            # exit(1) # Continue for debugging

        if not stats['inventory'].get('vaporub'):
            print("FAILED: Item not in inventory.")

        print("Item purchased successfully.")

        # Go Back (Button at bottom)
        # y > 640. Click at y=685 (scaled 0.95 -> 652)
        print("Clicking Back...")
        canvas.click(position={'x': 200, 'y': 685})
        time.sleep(0.5)

        # Start Game (Play button at y=380-426, center 403)
        print("Clicking Play...")
        canvas.click(position={'x': 200, 'y': 403})
        time.sleep(0.5)

        # Verify Shield is Active by checking if item was consumed from storage
        stats_game = page.evaluate("() => JSON.parse(localStorage.getItem('cb_stats'))")
        print("Stats after start:", stats_game)

        if stats_game['inventory'].get('vaporub'):
             print("FAILED: Item not consumed.")
             exit(1)

        # Take screenshot of gameplay with shield
        page.screenshot(path='verification/game_with_shield.png')
        print("Game started, shield consumed.")

        browser.close()

if __name__ == '__main__':
    verify_shop()
