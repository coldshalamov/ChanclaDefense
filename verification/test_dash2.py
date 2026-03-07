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

        # Click to start. The play button is at specific coordinates!
        page.mouse.click(200, 400)
        time.sleep(1)

        # Trigger dash to the right by pressing Right Arrow twice quickly
        page.keyboard.press("ArrowRight")
        page.keyboard.up("ArrowRight")
        time.sleep(0.1)
        page.keyboard.press("ArrowRight")
        page.keyboard.up("ArrowRight")

        # Wait a tiny bit for the dash to process and set opacity
        time.sleep(0.1)

        # Screenshot during dash
        page.screenshot(path="verification/dash_screenshot2.png")
        print("Dash screenshot saved to verification/dash_screenshot2.png")

        browser.close()

if __name__ == "__main__":
    run()
