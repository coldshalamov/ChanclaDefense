import sys

with open('verification/test_special.py', 'r') as f:
    content = f.read()

# According to memory:
# "To inject test functions (like `window.setSpecial` or custom game triggers) into the `index.html` IIFE for Playwright testing, tests often read the file, inject definitions using `content.rsplit('initTitle();', 1)`, and write the patched script to a temporary file before execution."
content_new = """from playwright.sync_api import sync_playwright
import time
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 450, 'height': 800}) # approximate mobile size
        page = context.new_page()

        cwd = os.getcwd()

        # Inject test functions
        with open('index.html', 'r') as f:
            html = f.read()

        injection = \"\"\"
        window.setSpecial = (val) => { specialAttackBar = val; };
        window.fireSpecial = () => { fireSpecialAttack(); };
        initTitle();
        \"\"\"
        patched_html = html.rsplit('initTitle();', 1)[0] + injection + html.rsplit('initTitle();', 1)[1]

        with open('test_index_special.html', 'w') as f:
            f.write(patched_html)

        page.goto(f"file://{cwd}/test_index_special.html")

        page.wait_for_selector("#game")

        # Start game
        page.mouse.click(200, 400)
        time.sleep(1)

        # Set special bar
        page.evaluate("window.setSpecial(100)")
        time.sleep(0.5)

        # Fire special
        page.evaluate("window.fireSpecial()")
        time.sleep(0.2)

        page.screenshot(path="verification/special_attack_leg.png")

        browser.close()

if __name__ == "__main__":
    run()
"""

with open('verification/test_special.py', 'w') as f:
    f.write(content_new)
