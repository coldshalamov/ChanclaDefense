
from playwright.sync_api import sync_playwright
import time
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 450, 'height': 800}) # approximate mobile size
        page = context.new_page()

        cwd = os.getcwd()
        page.goto(f"file://{cwd}/index.html")

        # Test scripts must inject debug functions because earlier global test hooks were removed.
        # We need to extract the script content, replace it, and execute it.
        script_content = page.locator("script").inner_text()
        injected_script = script_content.replace(
            "function initTitle() {",
            "window.setSpecial = function(val) { specialAttackBar = val; }; window.fireSpecial = fireSpecialAttack; function initTitle() {"
        )
        page.evaluate(injected_script)

        # Click the Play Button
        # The play button is at approx (110, 380, w, 46) but centers at x=200, y=400 on 400x700
        page.mouse.click(200, 400)

        time.sleep(1)

        # Cheat to fill special bar and ensure game is playing
        # We can also force state if the click failed for some reason, but let's try to be organic first.

        # Set special bar
        page.evaluate("window.setSpecial(100)")
        time.sleep(0.5)

        # Fire special
        page.evaluate("window.fireSpecial()")

        # Wait a few frames for the projectile to appear and move
        time.sleep(0.2)

        page.screenshot(path="verification/special_attack_leg.png")

        browser.close()

if __name__ == "__main__":
    run()
