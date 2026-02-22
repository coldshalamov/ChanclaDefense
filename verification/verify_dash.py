
from playwright.sync_api import sync_playwright
import time
import os

def verify_dash():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        cwd = os.getcwd()
        page.goto('file://' + cwd + '/index.html')

        # Start game
        canvas = page.locator('#game')
        canvas.click(position={'x': 200, 'y': 400})
        time.sleep(1) # Wait for start animation/dialogue

        # Check initial state
        dash_timer = page.evaluate("window.gameInternals.player.dash.timer")
        print(f"Initial dash timer: {dash_timer}")
        assert dash_timer == 0

        # Get initial X position
        initial_x = page.evaluate("window.gameInternals.player.x")
        print(f"Initial X: {initial_x}")

        # Trigger Dash (Shift)
        page.keyboard.press("Shift")

        # Check if dash active immediately
        time.sleep(0.05) # Allow 1 frame
        dash_timer_active = page.evaluate("window.gameInternals.player.dash.timer")
        dash_cooldown_active = page.evaluate("window.gameInternals.player.dash.cooldown")
        current_x = page.evaluate("window.gameInternals.player.x")

        print(f"Active dash timer: {dash_timer_active}")
        print(f"Active dash cooldown: {dash_cooldown_active}")
        print(f"Current X: {current_x}")

        if dash_timer_active > 0:
            print("SUCCESS: Dash timer activated.")
        else:
            print("FAILURE: Dash timer NOT activated.")
            exit(1)

        if abs(current_x - initial_x) > 10:
             print("SUCCESS: Player moved significantly (Dash speed).")
        else:
             print("WARNING: Player didn't move much, maybe direction was 0?")

        # Take screenshot
        page.screenshot(path='verification/dash_active.png')

        # Wait for cooldown
        time.sleep(1.0)
        dash_cooldown_end = page.evaluate("window.gameInternals.player.dash.cooldown")
        print(f"End dash cooldown: {dash_cooldown_end}")

        if dash_cooldown_end <= 0:
            print("SUCCESS: Cooldown reset.")
        else:
            print("FAILURE: Cooldown stuck?")

        browser.close()

if __name__ == "__main__":
    verify_dash()
