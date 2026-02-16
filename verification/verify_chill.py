from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        # Load the local file. Absolute path is safer.
        cwd = os.getcwd()
        page.goto(f"file://{cwd}/verification/verify_chill.html")

        # Wait a bit for the game to render and the pulse to be visible
        page.wait_for_timeout(1000)

        page.screenshot(path="verification/chill_before.png")
        browser.close()

if __name__ == "__main__":
    run()
