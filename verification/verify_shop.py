import time
from playwright.sync_api import sync_playwright
import os

def verify_shop():
    filepath = "file://" + os.path.abspath("index.html")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Using dimensions similar to what the original verify_game.py does
        context = browser.new_context(viewport={'width': 800, 'height': 800})
        page = context.new_page()

        page.goto(filepath)
        time.sleep(1)

        # Override the game state via Javascript
        page.evaluate("""() => {
            const data = { coins: 1000, upgrades: { lives: 0, shield: 0, cooldown: 0, luck: 0 }, bestScore: 0 };
            localStorage.setItem('chancla_bomb_save', JSON.stringify(data));
        }""")

        page.goto(filepath)
        time.sleep(1)

        # We need to click exactly on the coordinates relative to the bounding box of the canvas.
        # But `canvas.click(position={})` uses the canvas bounding box, which scales down depending on viewport width and height.
        # Because we're simulating a click, it might be easier to trigger the state change manually to see the shop,
        # rather than guessing the scaled bounding box math since the CSS `aspect-ratio: 4 / 7` and `width: min(95vw, 420px)`
        # make it complicated in Playwright.

        page.evaluate("""() => {
            // Because state is trapped in the IIFE, let's just trigger a click event precisely at the canvas coordinates
            // by reverse-engineering the scaling.
            const canvas = document.getElementById('game');
            const rect = canvas.getBoundingClientRect();
            const scaleX = canvas.width / rect.width;
            const scaleY = canvas.height / rect.height;

            // Target the shop button: 110, 450, w, 46 -> Center is 200, 473
            // Convert canvas coordinates to client coordinates
            const clientX = rect.left + 200 / scaleX;
            const clientY = rect.top + 473 / scaleY;

            const event = new MouseEvent('click', {
                clientX: clientX,
                clientY: clientY,
                bubbles: true
            });
            canvas.dispatchEvent(event);
        }""")

        time.sleep(1)
        screenshot_path = "verification/shop_verification.png"
        page.screenshot(path=screenshot_path)
        print(f"Shop screenshot taken: {screenshot_path}")

        page.evaluate("""() => {
            const canvas = document.getElementById('game');
            const rect = canvas.getBoundingClientRect();
            const scaleX = canvas.width / rect.width;
            const scaleY = canvas.height / rect.height;

            // Target the first upgrade: y=140, height=70 -> Center is 200, 175
            const clientX = rect.left + 200 / scaleX;
            const clientY = rect.top + 175 / scaleY;

            const event = new MouseEvent('click', {
                clientX: clientX,
                clientY: clientY,
                bubbles: true
            });

            canvas.dispatchEvent(event);
            canvas.dispatchEvent(event); // Second click
        }""")

        time.sleep(1)

        screenshot_path_2 = "verification/shop_upgraded.png"
        page.screenshot(path=screenshot_path_2)
        print(f"Shop upgraded screenshot taken: {screenshot_path_2}")

        browser.close()

if __name__ == "__main__":
    verify_shop()
