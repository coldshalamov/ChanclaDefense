
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

        # Click the canvas to start
        # The event listener is on the canvas and triggers on any click in TITLE state
        page.click("#game")

        time.sleep(1)

        # Cheat to fill special bar and ensure game is playing
        # We can also force state if the click failed for some reason, but let's try to be organic first.

        # Set special bar
        page.evaluate("window.setSpecial(100)")
        time.sleep(0.5)

        # Fire special
        page.evaluate("window.fireSpecial()")

        # Wait a few frames for the projectile to appear and move
        time.sleep(0.2)

        page.screenshot(path="verification/special_attack_leg.png")

        browser.close()

if __name__ == "__main__":
    run()
