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

        # Start game by clicking exactly on the Play button
        page.mouse.click(200, 400)

        time.sleep(0.5)

        # Force a chancla to spawn right next to the player (grazing distance)
        page.evaluate("""
            window.gameInternals = window.gameInternals || {};
            // We need to inject a chancla close to the player
            // But game logic is in IIFE. We can't access it easily.
            // Let's just wait for a chancla to naturally fall and move the player close to it.
        """)

        # Actually, since we can't easily access the IIFE to force a graze,
        # let's just hold the left arrow key to move the player to the left edge
        # and wait for chanclas to fall. Given enough time, a graze is very likely.
        page.keyboard.down("ArrowLeft")
        time.sleep(0.5)
        page.keyboard.up("ArrowLeft")

        # Wait a bit for game to progress
        time.sleep(3)

        # Move right a bit
        page.keyboard.down("ArrowRight")
        time.sleep(0.5)
        page.keyboard.up("ArrowRight")

        time.sleep(3)

        page.screenshot(path="verification/graze_test.png")
        print("Screenshot taken.")

        browser.close()

if __name__ == "__main__":
    run()
