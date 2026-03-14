from playwright.sync_api import Page, expect, sync_playwright
import time
import os

def test_dash(page: Page):
    cwd = os.getcwd()
    page.goto(f"file://{cwd}/index.html")

    page.wait_for_selector("#game")
    page.click("#game")
    page.mouse.click(200, 400) # Play button

    time.sleep(1)

    # Double click left to trigger dash
    page.keyboard.press("ArrowLeft")
    time.sleep(0.05)
    page.keyboard.press("ArrowLeft")

    # Wait for dash to start
    time.sleep(0.1)

    page.screenshot(path="verification/dash_test.png")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 450, 'height': 800}) # approximate mobile size
        page = context.new_page()
        try:
            test_dash(page)
        finally:
            browser.close()