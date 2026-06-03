import os
import re
import time
from playwright.sync_api import sync_playwright

def verify_slowmo():
    # We must patch the index.html file to expose the variables and force slow mo to trigger
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Apply replacement string to trigger slow-motion logic directly in HTML
    # We'll just hook into the update loop directly
    patch = """
                if (state !== STATE.PLAYING) return;

                // --- INJECTED HOOK ---
                if (!window.hooked) {
                    window.hooked = true;
                    slowMoTimer = 1.5;
                    dashTimer = 0.5;
                    player.x = 200;
                    player.y = 600;
                    chanclas.push({ x: 200, y: 600, vx: 0, vy: 0, w: 32, h: 18, type: 'normal', rotation: 0, rotSpeed: 0, dodged: true });
                    floatTexts.push({ text: 'PERFECT DODGE!', x: player.x, y: player.y - 40, time: 1.8, max: 1.8 });
                }
                baseSpeed = 0;
                spawnInterval = 999;
                // ---------------------
    """
    content = content.replace("if (state !== STATE.PLAYING) return;", patch)

    # Save temporary file
    temp_file = os.path.abspath('verification/temp_test.html')
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(content)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto('file://' + temp_file)

        # Override random for predictability if needed
        page.evaluate("window.Math.random = function() { return 0.5; };")
        page.evaluate("window.getAudioContext = function() { return null; };")

        # Click Play button using canvas click at center
        page.locator('canvas#game').click(position={"x": 200, "y": 410})

        time.sleep(1.0) # Allow render

        screenshot_path = os.path.abspath('verification/slowmo_screenshot.png')
        page.screenshot(path=screenshot_path)
        print(f"Screenshot taken: {screenshot_path}")

        browser.close()

    # Clean up temp file
    os.remove(temp_file)

if __name__ == '__main__':
    verify_slowmo()
