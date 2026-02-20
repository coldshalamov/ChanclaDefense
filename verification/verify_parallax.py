
from playwright.sync_api import sync_playwright
import time
import os

def verify_parallax():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the game from the file directly using absolute path
        cwd = os.getcwd()
        page.goto('file://' + cwd + '/chancla_bomb.html')

        # Start game by clicking
        canvas = page.locator('#game')
        canvas.click()
        time.sleep(1) # Wait for game start

        # Screenshot 1: Center position
        page.screenshot(path='verification/parallax_center.png')
        print('Center state screenshot taken.')

        # Move Right for 2 seconds
        page.keyboard.down('ArrowRight')
        time.sleep(2)
        page.keyboard.up('ArrowRight')
        time.sleep(0.5)

        # Screenshot 2: Right position
        page.screenshot(path='verification/parallax_right.png')
        print('Right state screenshot taken.')

        browser.close()

if __name__ == '__main__':
    verify_parallax()
