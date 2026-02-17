from playwright.sync_api import sync_playwright
import time
import os

def verify_expressions():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the game from the file directly using absolute path
        cwd = os.getcwd()
        page.goto('file://' + cwd + '/index.html')

        # Start game by clicking (simulate touch/click)
        # Assuming the play button is at a certain location or clicking canvas is sufficient
        # In current index.html, click starts game. In future update, it might check coordinates.
        # So I should click specifically on the "Play" button coordinates.
        # Play button rect: x=110, y=380, w=canvas.width-220, h=46. Center approx (200, 403).
        page.mouse.click(200, 403)

        # Wait a bit for game to start
        time.sleep(1)

        # Take a screenshot of normal state
        page.screenshot(path='verification/normal.png')
        print('Normal state screenshot taken.')

        # Trigger Slap
        page.keyboard.press('Space')

        # Wait a tiny bit for the next frame render (approx 50ms)
        time.sleep(0.05)
        page.screenshot(path='verification/slap.png')
        print('Slap state screenshot taken.')

        browser.close()

if __name__ == '__main__':
    verify_expressions()
