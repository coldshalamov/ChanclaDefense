from playwright.sync_api import sync_playwright
import time
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 450, 'height': 800}) # approximate mobile size
        page = context.new_page()

        cwd = os.getcwd()
        page.goto(f"file://{cwd}/index.html")

        # Wait for canvas
        page.wait_for_selector("#game")

        # Click the specific start button location
        page.mouse.click(x=200, y=400)

        time.sleep(1)

        # Apply a taco powerup (which we just removed support for)
        page.evaluate("window.applyPowerup({kind: 'taco', x: 200, y: 350})")

        # Apply a heart powerup to show powerups still work
        page.evaluate("window.applyPowerup({kind: 'heart', x: 200, y: 350})")

        # Wait a moment for float texts
        time.sleep(0.5)

        page.screenshot(path="verification/verify_no_taco.png")

        browser.close()

if __name__ == "__main__":
    run()
