import os
import time
from playwright.sync_api import sync_playwright, expect

def verify_dash():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Create context with touch support to test mobile controls
        context = browser.new_context(
            viewport={'width': 400, 'height': 700},
            has_touch=True,
            is_mobile=True
        )
        page = context.new_page()

        # Load the game from the local file (running from /app/verification)
        url = "file://" + os.path.abspath("../index.html")
        page.goto(url)

        # Start game by hitting Enter
        page.keyboard.press('Enter')
        page.wait_for_timeout(500) # wait for game to start

        # Take a screenshot before dash
        page.screenshot(path="pre_dash.png")

        # Double tap left arrow to dash left
        page.keyboard.press('ArrowLeft')
        page.wait_for_timeout(50)
        page.keyboard.press('ArrowLeft')

        # Wait a tiny bit for the dash effect to show
        page.wait_for_timeout(50)

        # Take screenshot of the dash effect (should see cyan trails)
        page.screenshot(path="dash_effect.png")

        # Wait for dash to finish
        page.wait_for_timeout(500)

        # Try touch dash right
        box = page.locator('.touch-right').bounding_box()
        if box:
            x = box['x'] + box['width'] / 2
            y = box['y'] + box['height'] / 2

            # Double tap using mouse to simulate touch
            page.mouse.click(x, y)
            page.wait_for_timeout(50)
            page.mouse.click(x, y)

            page.wait_for_timeout(50)
            page.screenshot(path="touch_dash_effect.png")

        browser.close()

if __name__ == "__main__":
    verify_dash()
    print("Screenshots taken.")
