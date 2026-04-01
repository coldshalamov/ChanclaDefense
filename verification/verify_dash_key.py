import os
from playwright.sync_api import sync_playwright

def verify_dash_key():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        file_path = f"file://{os.path.abspath('index.html')}"

        page.goto(file_path)

        # Override IIFE state
        page.evaluate("""
            const script = document.querySelector('script').textContent;
            const newScript = script.replace('initTitle();\\n        })();', 'initTitle(); window.player = player; window.dashTrails = dashTrails; })();');
            const scriptEl = document.createElement('script');
            scriptEl.textContent = newScript;
            document.body.appendChild(scriptEl);
        """)

        # Start game
        page.keyboard.press('Enter')
        page.wait_for_timeout(500)

        # Ensure we're in PLAYING state
        # the evaluate script may have launched two instances, but we'll try to trigger Shift on whatever is listening

        # Override dash cooldown to be sure
        page.evaluate("window.player.dashCooldown = 0;")

        page.keyboard.down('ArrowRight')
        page.wait_for_timeout(50)
        page.keyboard.down('Shift')
        page.wait_for_timeout(20)
        page.keyboard.up('Shift')
        page.keyboard.up('ArrowRight')

        # Take screenshot exactly when timer is > 0
        page.wait_for_timeout(50)

        dash_timer = page.evaluate('window.player.dashTimer')
        dash_trails_len = page.evaluate('window.dashTrails.length')

        screenshot_path = os.path.abspath('verification/dash_key_verification.png')
        page.screenshot(path=screenshot_path)

        print(f"Key Dash - Timer: {dash_timer}, Trails: {dash_trails_len}")
        browser.close()
        return screenshot_path

if __name__ == "__main__":
    verify_dash_key()
