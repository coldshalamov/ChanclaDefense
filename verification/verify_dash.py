import os
import time
from playwright.sync_api import sync_playwright

def verify_dash(page):
    # Construct an absolute file URL for index.html
    html_path = os.path.abspath('index.html')
    file_url = f"file://{html_path}"

    # 1. Load the page
    page.goto(file_url)
    page.wait_for_timeout(500)

    # Start game
    page.keyboard.press("Enter")
    page.wait_for_timeout(500)

    # Trigger dash right (double tap d)
    page.keyboard.press("d")
    page.wait_for_timeout(50)
    page.keyboard.press("d")
    page.wait_for_timeout(50) # wait a tiny bit for it to move

    # Screenshot dash state
    page.screenshot(path="verification/dash_state.png")
    print("Dash state screenshot taken at verification/dash_state.png")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            verify_dash(page)
        finally:
            browser.close()
