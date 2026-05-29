import os
import re
import time
from playwright.sync_api import sync_playwright

def run():
    with open('index.html', 'r') as f:
        content = f.read()

    # Provide window global assignment without altering IIFE since replacing 'let' might break things with syntax errors
    # Let's inject a cheat logic directly in the main update loop instead.

    cheat_script = """
    if (window.cheatActivated) {
        isa.anger = 10;
        isa.enraged = true;
        suegraTimer = 16;
        suegra.active = true;
        suegra.x = 200;
        suegra.y = 150;
        suegra.speed = 0;
        if (!window.cheatChanclaAdded) {
            chanclas.push({
                x: 200,
                y: 200,
                vx: 0,
                vy: 0,
                w: 32, h: 18, type: 'slipper', rotation: 0, rotSpeed: 0,
                isHoming: true
            });
            window.cheatChanclaAdded = true;
        }
    }
    """

    # inject into update(dt)
    content = content.replace("function update(dt) {", f"function update(dt) {{\n{cheat_script}")

    with open('verification/temp_test.html', 'w') as f:
        f.write(content)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        file_path = f"file://{os.path.abspath('verification/temp_test.html')}"
        page.goto(file_path)

        # Start game
        page.keyboard.press("Enter")
        page.wait_for_timeout(500)

        # Force suegra
        page.evaluate("window.cheatActivated = true")
        page.wait_for_timeout(500)

        page.screenshot(path="verification/suegra_screenshot.png")
        print("Screenshot saved to verification/suegra_screenshot.png")

        browser.close()

if __name__ == '__main__':
    run()
