
from playwright.sync_api import sync_playwright
import time
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 450, 'height': 800}) # approximate mobile size
        page = context.new_page()

        cwd = os.getcwd()

        # We need to inject a global reference
        with open("index.html", "r") as f:
            html = f.read()

        # Replace the final initTitle(); with initTitle(); window.debug_setSpecial = () => { specialAttackBar = 100; }; window.debug_fireSpecial = () => { fireSpecialAttack(); };
        html = html.replace('initTitle();\n        })();', 'initTitle();\n window.debug_setSpecial = () => { specialAttackBar = 100; }; window.debug_fireSpecial = () => { fireSpecialAttack(); };\n        })();')

        page.set_content(html)

        # Wait for canvas
        page.wait_for_selector("#game")

        # Click the canvas to start
        # The event listener is on the canvas and triggers on any click in TITLE state
        page.click("#game")

        time.sleep(1)

        # Cheat to fill special bar and ensure game is playing
        # We can also force state if the click failed for some reason, but let's try to be organic first.

        # Expose internal variables via injecting into the script and replacing the initTitle
        # We can just click the top half of the screen with a full bar to fire the special
        page.evaluate("() => { specialAttackBar = 100; }")
        time.sleep(0.5)

        # Fire special by simulating click or touch in the upper half
        page.keyboard.press(" ")

        # Wait a few frames for the projectile to appear and move
        time.sleep(0.2)

        page.screenshot(path="verification/special_attack_leg.png")

        browser.close()

if __name__ == "__main__":
    run()
