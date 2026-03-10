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

        page.wait_for_selector("#game")
        # Need precise click to hit the Play button, defaulting to center hit Play well enough
        page.mouse.click(200, 400)
        time.sleep(1)

        # Send 'ArrowLeft' twice quickly to trigger dash left
        page.keyboard.press("ArrowLeft")
        page.keyboard.press("ArrowLeft")

        # Give it a tiny bit of time to spawn the particles and move
        time.sleep(0.1)

        page.screenshot(path="verification/dash_mechanic.png")

        browser.close()

if __name__ == "__main__":
    run()
