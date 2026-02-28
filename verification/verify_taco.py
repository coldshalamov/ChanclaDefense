from playwright.sync_api import sync_playwright
import os

def test_taco():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        url = "file://" + os.path.abspath("index.html")
        page.goto(url)

        # Wait for the game canvas to load
        page.wait_for_selector("canvas#game")

        # Start game by clicking on the Play button roughly
        page.mouse.click(200, 400)

        # Take screenshot of running game
        page.wait_for_timeout(2000)
        page.screenshot(path="verification/taco_bomb.png")
        print("Screenshot taken: verification/taco_bomb.png")

        browser.close()

if __name__ == "__main__":
    test_taco()
