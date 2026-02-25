from playwright.sync_api import sync_playwright
import time
import os
import math

def verify_graze_visual():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Set viewport to a standard mobile-ish size to ensure consistent layout
        page = browser.new_page(viewport={'width': 450, 'height': 800})

        # Load the game
        cwd = os.getcwd()
        page.goto('file://' + cwd + '/chancla_bomb.html')

        # Wait for load
        page.wait_for_timeout(1000)

        # Locate the canvas
        canvas = page.locator("#game")
        box = canvas.bounding_box()
        if not box:
            print("Canvas not found!")
            browser.close()
            return

        print(f"Canvas box: {box}")

        # Calculate click position (proportional)
        # Play button center is approx 200/400 X, 403/700 Y
        click_x = box["x"] + box["width"] * 0.5
        click_y = box["y"] + box["height"] * (403 / 700)

        print(f"Clicking at: {click_x}, {click_y}")
        page.mouse.click(click_x, click_y)

        # Wait for game to start
        page.wait_for_timeout(1000)

        # Take a screenshot to verify game started
        page.screenshot(path='verification/game_start_check.png')
        print("Game start check screenshot taken.")

        # Main Loop:
        # The game runs. We need a chancla to get close (75px) but not hit.
        # This is hard to guarantee randomly.
        # But since we control the code, we can just hope/wait, or we can use the console to force it?
        # The prompt says "implement 1 change... verify".
        # We can't easily inject code in a "visual verify" script without changing the game.
        # We'll just run for a while and take screenshots. The Graze mechanic prints text "GRAZE! +15".
        # We will look for that text in the screenshots.

        print("Capturing gameplay screenshots...")
        for i in range(20):
            # Simulate some movement to avoid getting hit constantly?
            # Or just stay still. Center is safe-ish early on.

            timestamp = int(time.time() * 100)
            filename = f"verification/graze_attempt_{timestamp}.png"
            page.screenshot(path=filename)
            # print(f"Saved {filename}")

            # Wait a bit (simulating frame gap)
            page.wait_for_timeout(200)

        browser.close()

if __name__ == '__main__':
    verify_graze_visual()
