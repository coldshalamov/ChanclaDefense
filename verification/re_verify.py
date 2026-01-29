
import os
from playwright.sync_api import sync_playwright

def verify():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        path = os.path.abspath('chancla_bomb.html')
        page.goto(f'file://{path}')

        page.wait_for_timeout(1000)
        page.screenshot(path='verification/title_screen.png')
        browser.close()

if __name__ == "__main__":
    verify()
