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

        # Click the canvas to start
        page.click("#game", position={"x": 200, "y": 400}) # Click Play

        time.sleep(1)

        # Trigger dash by pressing Right twice quickly
        page.keyboard.press("ArrowRight")
        page.keyboard.press("ArrowRight")

        # Wait a tiny bit for the visual effect (opacity and particles)
        time.sleep(0.05)

        page.screenshot(path="verification/dash_verification.png")

        browser.close()

if __name__ == "__main__":
    run()
