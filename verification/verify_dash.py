import os
import time
from playwright.sync_api import sync_playwright

def verify_dash():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Using a mobile context to easily verify the mobile double-tap dash
        context = browser.new_context(
            viewport={'width': 390, 'height': 844},
            is_mobile=True,
            has_touch=True
        )
        page = context.new_page()
        file_path = f"file://{os.path.abspath('index.html')}"
        page.goto(file_path)

        # Expose state to window object for testing
        page.evaluate("""
            const script = document.querySelector('script').textContent;
            const newScript = script.replace('})();', 'window.player = player; window.dashTrails = dashTrails; })();');
            eval(newScript);
        """)

        # Start game by simulating enter key
        page.keyboard.press('Enter')
        page.wait_for_timeout(500)

        # Double tap left zone to trigger dash
        left_zone = page.locator('.touch-left')

        # First tap
        left_zone.tap()
        page.wait_for_timeout(50) # Small delay
        # Second tap
        left_zone.tap()

        # Take screenshot immediately to capture ghosting trail
        page.wait_for_timeout(100) # Give it just a moment to render trails

        screenshot_path = os.path.abspath('verification/dash_verification.png')
        page.screenshot(path=screenshot_path)

        # Check if dash was triggered
        dash_timer = page.evaluate('window.player.dashTimer')
        dash_trails = page.evaluate('window.dashTrails.length')

        print(f"Dash Timer after double tap: {dash_timer}")
        print(f"Dash Trails active: {dash_trails}")

        if dash_timer > 0 and dash_trails > 0:
            print("SUCCESS: Dash triggered successfully.")
        else:
            print("WARNING: Dash did not trigger or trails not rendered.")

        browser.close()
        return screenshot_path

if __name__ == "__main__":
    verify_dash()
