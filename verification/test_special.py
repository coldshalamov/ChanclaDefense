
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

        # Wait for canvas
        page.wait_for_selector("#game")

        # Click the canvas to start
        # The event listener is on the canvas and triggers on any click in TITLE state
        page.click("#game")

        time.sleep(1)

        # Cheat to fill special bar and ensure game is playing
        # We can also force state if the click failed for some reason, but let's try to be organic first.

        # Modify html to expose internal functions to window for testing
        with open("index.html", "r") as f:
            content = f.read()

        content = content.replace(
            "initTitle();",
            "initTitle();\nwindow.setSpecial = (val) => { specialAttackBar = val; };\nwindow.fireSpecial = () => { fireSpecialAttack(); };"
        )

        with open("index.html", "w") as f:
            f.write(content)

        page.reload()
        page.wait_for_selector("#game")

        # Click the Play Button (approx 200, 400 on 400x700 scaled canvas)
        box = page.locator("#game").bounding_box()
        page.mouse.click(box['x'] + 200 * (box['width'] / 400), box['y'] + 400 * (box['height'] / 700))

        time.sleep(1)

        # Set special bar
        page.evaluate("window.setSpecial(100)")
        time.sleep(0.5)

        # Fire special
        page.evaluate("window.fireSpecial()")

        # Restore index.html
        with open("index.html", "r") as f:
            content = f.read()
        content = content.replace(
            "initTitle();\nwindow.setSpecial = (val) => { specialAttackBar = val; };\nwindow.fireSpecial = () => { fireSpecialAttack(); };",
            "initTitle();"
        )
        with open("index.html", "w") as f:
            f.write(content)

        # Wait a few frames for the projectile to appear and move
        time.sleep(0.2)

        page.screenshot(path="verification/special_attack_leg.png")

        browser.close()

if __name__ == "__main__":
    run()
