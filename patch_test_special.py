import re

with open('verification/test_special.py', 'r') as f:
    content = f.read()

new_content = """
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

        # Expose specialAttackBar and fireSpecialAttack
        page.evaluate('''() => {
            const scripts = document.querySelectorAll('script');
            let content = scripts[scripts.length - 1].textContent;

            // Expose variables
            content = content.replace('let specialAttackBar = 0;', 'window.specialAttackBar = 0;');
            content = content.replace('specialAttackBar = Math.min', 'window.specialAttackBar = Math.min');
            content = content.replace('if (specialAttackBar >= maxSpecialAttack)', 'if (window.specialAttackBar >= maxSpecialAttack)');
            content = content.replace('specialAttackBar = 0;', 'window.specialAttackBar = 0;');
            content = content.replace('const p = Math.min(1, specialAttackBar / maxSpecialAttack);', 'const p = Math.min(1, window.specialAttackBar / maxSpecialAttack);');

            content = content.replace('function fireSpecialAttack() {', 'window.fireSpecialAttack = function() {');

            // Add helpers
            content = content.replace('initTitle();', 'initTitle(); window.setSpecial = (val) => { window.specialAttackBar = val; }; window.fireSpecial = () => { window.fireSpecialAttack(); };');

            // Remove old script and inject modified one
            scripts[scripts.length - 1].remove();
            const newScript = document.createElement('script');
            newScript.textContent = content;
            document.body.appendChild(newScript);
        }''')

        # Wait for canvas
        page.wait_for_selector("#game")

        # Click the canvas to start
        # The event listener is on the canvas and triggers on any click in TITLE state
        # Coordinates must match Play Button (110, 380, w, 46) mapped to canvas internal resolution
        box = page.locator("#game").bounding_box()
        page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] * (400 / 700))

        time.sleep(1)

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
"""

with open('verification/test_special.py', 'w') as f:
    f.write(new_content)
