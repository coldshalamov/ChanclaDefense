from playwright.sync_api import sync_playwright
import time
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 450, 'height': 800}) # approximate mobile size
        page = context.new_page()

        cwd = os.getcwd()

        # The internal game state is wrapped in an IIFE. Since earlier global test hooks (like window.setSpecial) were removed, Playwright test scripts must inject debug functions dynamically by replacing code like the final initTitle(); call in the HTML string.
        with open("index.html", "r") as f:
            content = f.read()

        # Inject debug functions
        content = content.replace("initTitle();", """
            initTitle();
            window.debug_setSpecial = (val) => { specialAttackBar = val; };
            window.debug_fireSpecial = () => { fireSpecialAttack(); };
        """)

        # Set route to serve modified HTML
        page.route("**/*", lambda route: route.fulfill(body=content, content_type="text/html"))

        page.goto(f"http://localhost/index.html")

        # Wait for canvas
        page.wait_for_selector("#game")

        # Click the canvas to start
        # The event listener is on the canvas and triggers on any click in TITLE state
        page.click("#game")
        # Need to click at explicit coordinates for Play button
        page.mouse.click(200, 400)

        time.sleep(1)

        # Set special bar
        page.evaluate("window.debug_setSpecial(100)")
        time.sleep(0.5)

        # Fire special
        page.evaluate("window.debug_fireSpecial()")

        # Wait a few frames for the projectile to appear and move
        time.sleep(0.2)

        page.screenshot(path="verification/special_attack_leg.png")

        browser.close()

if __name__ == "__main__":
    run()