
from playwright.sync_api import sync_playwright
import time
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        cwd = os.getcwd()
        page.goto(f'file://{cwd}/index.html')
        page.click('#game')
        time.sleep(1)
        page.screenshot(path='verification/game_running.png')
        browser.close()

if __name__ == '__main__':
    run()
