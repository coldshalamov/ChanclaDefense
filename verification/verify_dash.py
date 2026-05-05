import os
import time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        url = "file://" + os.path.abspath('index.html')
        page.goto(url)

        # Start game
        page.keyboard.press('Enter')
        time.sleep(0.5)

        # Trigger dash left
        page.keyboard.press('a')
        page.keyboard.up('a')
        time.sleep(0.05)
        page.keyboard.press('a')
        page.keyboard.up('a')

        time.sleep(0.1) # Wait briefly so dash trails appear

        page.screenshot(path='verification/dash_verification.png')

        # Take a screenshot
        print("Screenshot saved to verification/dash_verification.png")
        browser.close()

if __name__ == '__main__':
    run()
