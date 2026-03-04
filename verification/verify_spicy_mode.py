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

        # Let's dynamically modify the script to expose player
        content = page.content()
        new_content = content.replace("const player =", "window.player =")
        page.set_content(new_content)

        # Wait for canvas
        page.wait_for_selector("#game")
        time.sleep(1)

        # Click the canvas to start (the button is at ~ y: 400)
        page.mouse.click(200, 400)
        time.sleep(1)

        page.evaluate("window.player.chiliTimer = 6;")

        time.sleep(0.5)

        page.screenshot(path="verification/spicy_mode.png")
        print("Spicy mode screenshot taken.")

        browser.close()

if __name__ == "__main__":
    run()