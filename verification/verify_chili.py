from playwright.sync_api import sync_playwright
import time
import os

def verify_chili():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the game from the file directly using absolute path
        cwd = os.getcwd()
        page.goto('file://' + cwd + '/index.html')

        # Start game by clicking (simulate touch/click)
        canvas = page.locator('#game')
        canvas.click(position={'x': 200, 'y': 400}) # Play button

        # Wait a bit for game to start
        time.sleep(1)

        # Inject JS to set chili timer
        print("Injecting Chili Timer...")
        page.evaluate("window.gameInternals.player.chiliTimer = 5")

        # Wait a bit to let the effect run
        time.sleep(0.5)

        # Take a screenshot to see if player is red/spicy
        page.screenshot(path='verification/chili_effect.png')
        print("Screenshot saved to verification/chili_effect.png")

        # Verify timer is decreasing
        timer_val = page.evaluate("window.gameInternals.player.chiliTimer")
        print(f"Current Chili Timer: {timer_val}")
        if timer_val > 0 and timer_val < 5:
            print("SUCCESS: Timer is active and decreasing.")
        else:
            print(f"FAILURE: Timer is {timer_val}, expected between 0 and 5.")

        browser.close()

if __name__ == '__main__':
    verify_chili()
