from playwright.sync_api import sync_playwright
import time
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 450, 'height': 800})
        page = context.new_page()

        cwd = os.getcwd()
        page.goto(f"file://{cwd}/index.html")

        # Wait for canvas
        page.wait_for_selector("#game")

        # Click the Play button
        page.mouse.click(200, 400)
        time.sleep(1)

        # Trigger double tap left to dash
        page.keyboard.down("ArrowLeft")
        time.sleep(0.05)
        page.keyboard.up("ArrowLeft")

        time.sleep(0.05)

        page.keyboard.down("ArrowLeft")
        time.sleep(0.05)
        page.keyboard.up("ArrowLeft")

        # Take screenshot during dash
        time.sleep(0.1)
        page.screenshot(path="verification/dash_mechanic.png")

        browser.close()

if __name__ == "__main__":
    run()
