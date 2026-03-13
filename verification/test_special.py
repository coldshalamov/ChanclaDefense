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

        # Inject debug functions
        content = page.content()
        content = content.replace("initTitle();", """
            initTitle();
            window.setSpecial = (val) => { specialAttackBar = val; };
            window.fireSpecial = fireSpecialAttack;
        """)
        page.set_content(content)

        # Click the canvas to start
        page.mouse.click(200, 400) # Play button coordinates

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
