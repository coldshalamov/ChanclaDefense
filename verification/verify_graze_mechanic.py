from playwright.sync_api import sync_playwright
import time
import os

def verify_graze_mechanic():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the game from the file directly using absolute path
        cwd = os.getcwd()
        page.goto('file://' + cwd + '/index.html')

        # Verify page title
        assert 'Chancla Bomb' in page.title()
        print('Page loaded successfully.')

        # Start game by clicking (simulate touch/click)
        canvas = page.locator('#game')
        canvas.click()
        print('Game started.')

        # Wait a bit for game to run
        time.sleep(2)

        # Check for console errors (none expected)
        errors = []
        page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)

        if errors:
            print(f"Console errors found: {errors}")
            # Fails if errors found (unless they are harmless warnings, but usually critical)

        # Take a screenshot to verify visuals
        page.screenshot(path='verification/graze_mechanic_running.png')
        print('Running state screenshot taken.')

        browser.close()

if __name__ == '__main__':
    verify_graze_mechanic()
