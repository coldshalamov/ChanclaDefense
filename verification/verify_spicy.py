from playwright.sync_api import sync_playwright
import time
import os

def verify_spicy():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        cwd = os.getcwd()
        page.goto('file://' + cwd + '/chancla_bomb.html')

        # Start game
        canvas = page.locator('#game')
        canvas.click(position={"x": 200, "y": 400})
        time.sleep(1)

        # Inject Spicy Mode
        print("Injecting Spicy Mode...")
        page.evaluate('window.gameInternals.player.chiliTimer = 5')

        # Verify Timer
        timer = page.evaluate('window.gameInternals.player.chiliTimer')
        print(f"Chili Timer: {timer}")
        assert timer > 0, "Chili timer should be active"

        # Wait and verify decrement
        time.sleep(0.5)
        timer_after = page.evaluate('window.gameInternals.player.chiliTimer')
        print(f"Chili Timer after 0.5s: {timer_after}")
        assert timer_after < timer, "Timer should decrease"

        # Take screenshot
        page.screenshot(path='verification/spicy_mode.png')
        print('Spicy Mode screenshot taken.')

        browser.close()

if __name__ == '__main__':
    verify_spicy()
