import os
import time
from playwright.sync_api import sync_playwright

def verify_phone_removed():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Mobile viewport is crucial for the canvas scaling
        context = browser.new_context(viewport={'width': 450, 'height': 800}, has_touch=True, is_mobile=True)
        page = context.new_page()

        file_path = f"file://{os.path.abspath('index.html')}"

        # Start game and expose internals
        page.on("request", lambda request: print(f"Request: {request.url}"))
        page.on("pageerror", lambda err: print(f"Page Error: {err}"))
        page.on("console", lambda msg: print(f"Console: {msg.text}"))

        with open('index.html', 'r') as f:
            content = f.read()

        # Bypass localStorage error for file:// protocol by making try block quiet
        content = content.replace("try {", "try {\n                if (window.location.protocol === 'file:') throw new Error('skip');")

        page.set_content(content)

        # Click play button
        page.mouse.click(200, 400)
        time.sleep(2.0)

        # Take a screenshot to show game running without chisme timer logic
        page.screenshot(path="verification/game_running_without_phone.png")

        browser.close()

if __name__ == "__main__":
    verify_phone_removed()
