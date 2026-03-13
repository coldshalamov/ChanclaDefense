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

        # Click the Play Button (approx 200, 400 on 400x700 scaled canvas)
        box = page.locator("#game").bounding_box()
        page.mouse.click(box['x'] + 200 * (box['width'] / 400), box['y'] + 400 * (box['height'] / 700))

        time.sleep(1)

        # Trigger dash (double tap right)
        page.keyboard.press("ArrowRight")
        time.sleep(0.1)
        page.keyboard.press("ArrowRight")

        # Wait a few frames for the dash to start
        time.sleep(0.05)

        page.screenshot(path="verification/dash.png")

        browser.close()

if __name__ == "__main__":
    run()
