from playwright.sync_api import sync_playwright
import time
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 450, 'height': 800})
        page = context.new_page()

        cwd = os.getcwd()

        # Read the file and inject a patch to expose chanclas for testing
        with open("index.html", "r") as f:
            content = f.read()
        content = content.replace("let chanclas = [];", "window.chanclas = []; let chanclas = window.chanclas;")

        # We need to test the game, so we write this to a temporary file
        with open("verification/index_test.html", "w") as f:
            f.write(content)

        page.goto(f"file://{cwd}/verification/index_test.html")

        # Wait for canvas
        page.wait_for_selector("#game")

        # Click the play button (110, 380, w, 46) so at x=200, y=400
        page.click("#game", position={"x": 200, "y": 400})

        # Wait for game to start
        time.sleep(1)

        # Inject chancla close to player: x=250, y=660
        # Player is at x=200, y=630. dx=50, dy=30.
        # w/2 + w/2 = 27.5 + 16 = 43.5. dx > 43.5 -> 50 > 43.5 (No overlap)
        # dy=30. dist = sqrt(2500 + 900) = sqrt(3400) = 58 < 75. Graze!
        page.evaluate("""
            window.chanclas.push({ x: 250, y: 660, vx: 0, vy: 0, w: 32, h: 18, type: 'normal', rotation: 0, rotSpeed: 0 });
        """)

        # Run one frame update if possible. Actually the game loop runs automatically.
        time.sleep(0.1)

        page.screenshot(path="verification/graze_verification.png")

        browser.close()

if __name__ == "__main__":
    run()
