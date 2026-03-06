from playwright.sync_api import sync_playwright
import time
import os

def test_no_taco():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 450, 'height': 800})
        page = context.new_page()

        cwd = os.getcwd()
        page.goto(f"file://{cwd}/index.html")

        page.mouse.click(200, 400)

        # Override math random, speed up time elapsed, and force spawn of an Owen pet.
        # We need an Owen to spawn to drop the powerup.
        page.evaluate("""
            Math.random = () => 0.3;
        """)

        # Wait a bit
        time.sleep(3)

        page.screenshot(path="verification/no_taco.png")

        browser.close()

if __name__ == "__main__":
    test_no_taco()
