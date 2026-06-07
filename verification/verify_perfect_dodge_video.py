import re
from playwright.sync_api import sync_playwright
import os
import glob

def run_cuj(page):
    path = os.path.abspath('temp_test_dodge.html')
    page.goto(f'file://{path}')
    page.wait_for_timeout(500)

    # Click start area (not really title screen since we bypass, but just in case)
    page.mouse.click(200, 400)
    page.wait_for_timeout(500)

    # Take screenshot while the perfect dodge text and cyan flash is active
    os.makedirs('/home/jules/verification/screenshots', exist_ok=True)
    page.screenshot(path="/home/jules/verification/screenshots/perfect_dodge.png")
    page.wait_for_timeout(1000)

if __name__ == "__main__":
    with open('index.html', 'r') as f:
        content = f.read()

    # Inject the perfect dodge scenario directly into the update loop
    content = content.replace("function update(dt) {", """
        function update(dt) {
            if (!window.injectedDodge) {
                window.injectedDodge = true;
                player.x = 200;
                player.y = 600;
                dashTimer = 0.15; // Player is dashing
                chanclas = [{
                    x: 200, y: 600, w: 32, h: 18, type: 'normal', slapped: false, dodged: false, rotation: 0, rotSpeed: 0
                }];
                window.getSlowMo = () => slowMoTimer;
            }
    """)

    with open('temp_test_dodge.html', 'w') as f:
        f.write(content)

    os.makedirs('/home/jules/verification/videos', exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="/home/jules/verification/videos"
        )
        page = context.new_page()
        page.add_init_script("Object.defineProperty(window, 'localStorage', { value: { getItem: () => null, setItem: () => {} }, writable: true });")
        try:
            run_cuj(page)
        finally:
            context.close()
            browser.close()

    # Verify it actually triggered
    print("Video recorded to /home/jules/verification/videos")
