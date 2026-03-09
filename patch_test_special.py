import sys

def patch_file(filename):
    clean_code = """from playwright.sync_api import sync_playwright
import time
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 450, 'height': 800}) # approximate mobile size
        page = context.new_page()

        cwd = os.getcwd()
        page.goto('file://' + cwd + '/index.html')

        # We can extract and modify the script text content like memory says:
        # "To expose internal game state (like `player` or `chanclas`) for Playwright testing despite the IIFE, test scripts can dynamically extract and modify the DOM's <script> text content (e.g., content.replace('const player = {', 'window.player = {')) before evaluating it."

        script_content = page.locator("script").first.text_content()

        script_content = script_content.replace('let specialAttackBar = 0;', 'window.specialAttackBar = 0; let specialAttackBar = 0;')
        script_content = script_content.replace('specialAttackBar = Math.min', 'window.specialAttackBar = Math.min')
        script_content = script_content.replace('function fireSpecialAttack() {', 'window.fireSpecial = function() { specialAttackBar = 100; fireSpecialAttack(); }; function fireSpecialAttack() {')

        # Evaluating the script content directly
        page.evaluate(script_content)

        page.wait_for_selector("#game")
        page.locator("#game").click(position={"x": 200, "y": 400})
        time.sleep(1)

        page.evaluate("window.specialAttackBar = 100;")
        page.evaluate("window.fireSpecial()")
        time.sleep(0.2)

        page.screenshot(path="verification/special_attack_leg.png")
        browser.close()

if __name__ == "__main__":
    run()
"""
    with open(filename, 'w') as f:
        f.write(clean_code)

patch_file('verification/test_special.py')
