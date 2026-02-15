from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the game
        url = f"file://{os.getcwd()}/index.html"
        page.goto(url)

        # Click Tiendita button on Title Screen
        # Button is drawn at y=440, height=46. Canvas height=700.
        # We need to click within the canvas coordinates.
        # Playwright clicks relative to viewport, so we need to target the canvas.
        # But since we are loading file:// directly, the canvas is likely at top left or centered.
        # Let's target the canvas element and click relative to it.

        canvas = page.locator("#game")
        box = canvas.bounding_box()

        # Scale calculation if needed? Canvas is 400x700.
        # CSS width/height might be different.
        # In CSS: width: min(95vw, 420px); aspect-ratio: 4/7.
        # If viewport is large, it's 420px wide.
        # Internal width is 400.

        # We can just click relative to the bounding box.
        # Shop button internal coords: x=110, y=440, w=180, h=46 (canvas.width-220 = 400-220 = 180)
        # Center x = 200, y = 463.

        # Calculate relative position
        rel_x = 200 / 400 * box['width']
        rel_y = 463 / 700 * box['height']

        page.mouse.click(box['x'] + rel_x, box['y'] + rel_y)

        # Wait a bit for transition
        page.wait_for_timeout(500)

        # Screenshot Shop
        page.screenshot(path="verification/shop_screen.png")
        print("Shop screenshot taken.")

        # Click Back button
        # Internal coords: y=620 (700-80), h=46. Center y=643. x=200.
        rel_y_back = 643 / 700 * box['height']

        page.mouse.click(box['x'] + rel_x, box['y'] + rel_y_back)

        page.wait_for_timeout(500)
        page.screenshot(path="verification/back_to_title.png")
        print("Back to title screenshot taken.")

        browser.close()

if __name__ == "__main__":
    run()
