from playwright.sync_api import sync_playwright
import time
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 450, 'height': 800}) # approximate mobile size
        page = context.new_page()

        cwd = os.getcwd()
        page.goto('file://' + cwd + '/index.html')

        page.wait_for_selector("#game")
        # Click the play button
        page.locator("#game").click(position={"x": 200, "y": 400})
        time.sleep(1)

        # Double tap right
        page.keyboard.press("ArrowRight")
        time.sleep(0.1)
        page.keyboard.press("ArrowRight")

        # Wait a tiny bit for the dash to process
        time.sleep(0.1)

        # Take a screenshot to show the dash particle and translucency
        page.screenshot(path="verification/dash_verification.png")
        print("Screenshot taken: verification/dash_verification.png")
        browser.close()

if __name__ == "__main__":
    run()
