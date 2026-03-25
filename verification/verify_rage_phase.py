from playwright.sync_api import sync_playwright
import os
import time

def test_rage_phase():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 450, 'height': 800},
            has_touch=True,
            is_mobile=True
        )
        page = context.new_page()

        # Load the game locally
        file_path = 'file://' + os.path.abspath('chancla_bomb.html')

        # We need to modify the DOM slightly to expose game variables for the test
        # Read the HTML content
        with open('chancla_bomb.html', 'r') as f:
            content = f.read()

        # Expose isa and chanclas to window
        content = content.replace('const isa = {', 'window.isa = {')
        content = content.replace('let chanclas = [];', 'window.chanclas = []; let chanclas = window.chanclas;')
        content = content.replace('let specialAttackBar = 0;', 'window.specialAttackBar = 0; let specialAttackBar = window.specialAttackBar;')
        content = content.replace('initTitle();\n        })();', 'initTitle();\nwindow.startGameFromTitle = startGameFromTitle;        })();')

        page.set_content(content)
        time.sleep(1)

        # Click Play button
        # The button is at y=380-426, x=110 to width-110
        page.mouse.click(200, 400)
        time.sleep(1)

        # Force Isa into Rage Phase by setting anger low
        page.evaluate('window.isa.anger = 20;')

        # Wait a bit for the phase to trigger and chanclas to spawn
        time.sleep(3)

        # Take a screenshot
        os.makedirs('verification', exist_ok=True)
        screenshot_path = 'verification/rage_phase.png'
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

        browser.close()

if __name__ == '__main__':
    test_rage_phase()
