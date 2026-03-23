import os
from playwright.sync_api import sync_playwright

def verify_dash():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={'width': 450, 'height': 800})
        page = context.new_page()

        file_path = 'file://' + os.path.abspath('index.html')
        page.goto(file_path)

        # Start game by clicking exactly on the play button coordinates
        page.evaluate("document.elementFromPoint(200, 400).dispatchEvent(new MouseEvent('click', {clientX: 200, clientY: 400}))")

        page.wait_for_timeout(500)

        # Press right and dash
        page.keyboard.down('ArrowRight')
        page.keyboard.down('Shift')
        page.wait_for_timeout(50)

        page.screenshot(path="verification/dash_test.png")

        # Wait a bit more and take another screenshot
        page.wait_for_timeout(50)
        page.screenshot(path="verification/dash_test2.png")

        page.keyboard.up('Shift')
        page.keyboard.up('ArrowRight')

        browser.close()

if __name__ == "__main__":
    verify_dash()
