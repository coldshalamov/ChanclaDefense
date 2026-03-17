import os
import time
from playwright.sync_api import sync_playwright

def verify_achievements():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Mobile viewport since game is mobile-first
        context = browser.new_context(viewport={'width': 450, 'height': 800}, is_mobile=True, has_touch=True)
        page = context.new_page()

        file_url = 'file://' + os.path.abspath('index.html')
        page.goto(file_url)

        time.sleep(1) # Let it render

        # Dispatch a click exactly where the achievements button is
        page.evaluate('''() => {
            const canvas = document.getElementById('game');
            const rect = canvas.getBoundingClientRect();
            // Internal coords for achievements button are x: 110, y: 520, w: canvas.width - 220, h: 46
            // Let's click at internal center: x=200, y=543
            const targetX = rect.left + (200 / canvas.width) * rect.width;
            const targetY = rect.top + (543 / canvas.height) * rect.height;

            const event = new MouseEvent('click', {
                clientX: targetX,
                clientY: targetY,
                bubbles: true
            });
            canvas.dispatchEvent(event);
        }''')

        time.sleep(1) # Wait for render

        # Take screenshot of the achievements screen
        screenshot_path = 'verification/achievements_screen2.png'
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

        browser.close()

if __name__ == "__main__":
    verify_achievements()
