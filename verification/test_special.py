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

        # Expose internal game state for Playwright testing
        content = page.content()
        new_content = content.replace("let specialAttackBar = 0;", "window.specialAttackBar = 0; let specialAttackBar = 0;")
        new_content = new_content.replace("function fireSpecialAttack() {", "window.fireSpecial = fireSpecialAttack; function fireSpecialAttack() {")
        page.set_content(new_content)

        # Wait for canvas
        page.wait_for_selector("#game")

        # Click the canvas to start (Play Button is at approx 200, 400)
        page.mouse.click(200, 400)

        time.sleep(1)

        # Set special bar
        page.evaluate("window.specialAttackBar = 100")
        time.sleep(0.5)

        # Fire special
        page.evaluate("window.fireSpecial()")

        # Wait a few frames for the projectile to appear and move
        time.sleep(0.2)

        page.screenshot(path="verification/special_attack_leg.png")

        browser.close()

if __name__ == "__main__":
    run()
