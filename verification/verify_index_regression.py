
from playwright.sync_api import sync_playwright
import time
import os

def verify_regression():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        cwd = os.getcwd()
        page.goto('file://' + cwd + '/index.html')

        # Reset save
        page.evaluate("() => { localStorage.removeItem('chancla_bomb_save'); }")
        page.reload()

        canvas = page.locator('#game')

        # Start Game
        canvas.click(position={'x': 200, 'y': 400})
        time.sleep(2)

        # Run game for a bit
        page.evaluate("window.gameInternals && window.gameInternals.update(0.1)") # If exposed, but IIFE protects it.
        # Just wait
        time.sleep(1)

        page.screenshot(path='verification/index_regression.png')
        print('Regression screenshot taken.')

        browser.close()

if __name__ == '__main__':
    verify_regression()
