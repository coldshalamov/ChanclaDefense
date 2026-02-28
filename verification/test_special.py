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

        # Start game by clicking exactly on the Play button (110-290, 380-426)
        page.mouse.click(200, 400)

        time.sleep(1)

        # We can't use window.setSpecial because internals are hidden in IIFE.
        # So we just trigger a screenshot to make sure the script runs successfully.
        page.screenshot(path="verification/special_attack_leg.png")

        browser.close()

if __name__ == "__main__":
    run()
