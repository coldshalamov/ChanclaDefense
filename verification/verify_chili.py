from playwright.sync_api import sync_playwright
import time
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 450, 'height': 800})
        page = context.new_page()

        cwd = os.getcwd()

        # Read index.html directly and inject window variables for testing
        with open("index.html", "r") as f:
            html = f.read()

        # The game is wrapped in an IIFE, we need to carefully export player, chanclas, etc.
        html = html.replace('const player = {', 'window.player = {')
        html = html.replace('let chanclas = [];', 'window.chanclas = [];')
        html = html.replace('function trySlap() {', 'window.trySlap = function() {')

        with open("verification/test_index.html", "w") as f:
            f.write(html)

        page.goto(f"file://{cwd}/verification/test_index.html")

        # Wait for canvas
        page.wait_for_selector("#game")

        # Click the canvas to start. Use coordinates to hit "Jugar"
        page.click("#game", position={"x": 200, "y": 400})
        time.sleep(1)

        # Trigger chili powerup
        page.evaluate("""
            window.player.chiliTimer = 6;
            window.chanclas.push({ x: window.player.x, y: window.player.y - 20, vx: 0, vy: 0, w: 32, h: 18, type: 'normal', rotation: 0, rotSpeed: 0, slapped: false });
        """)

        time.sleep(0.1) # Wait a tick for update
        page.screenshot(path="verification/chili_spicy_mode.png")

        # Test perfect slap in spicy mode
        page.evaluate("window.trySlap();")
        time.sleep(0.1)
        page.screenshot(path="verification/chili_slap.png")

        browser.close()

if __name__ == "__main__":
    run()
