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

        # Expose internal game state
        content = page.content()
        new_content = content.replace("let specialAttackBar = 0;", "window.isa = isa; let specialAttackBar = 0;")
        page.set_content(new_content)

        # Wait for canvas
        page.wait_for_selector("#game")

        # Click the Play Button
        page.mouse.click(200, 400)

        time.sleep(1)

        # Trigger Rage Mode by setting anger low
        page.evaluate("window.isa.anger = 40;")

        # Wait a bit for the next update tick to process the anger drop and trigger rage mode visually
        time.sleep(0.5)

        page.screenshot(path="verification/rage_mode.png")

        browser.close()

if __name__ == "__main__":
    run()
