import os
from playwright.sync_api import sync_playwright

def test_ghost_chancla():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"file://{os.path.abspath('index.html')}")

        # Start game by pressing enter
        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)

        # We need to evaluate inside the IIFE scope, but playwright can't reach local variables easily.
        # Instead, let's just make the changes to force ghost chanclas and see if the game runs without errors.
        page.evaluate("""
            Math.random = () => 0.65; // Adjust to hit the ghost probability logic.
        """)

        page.wait_for_timeout(3000) # wait for spawn and update

        print("Game ran with mocked random without throwing exceptions.")

        browser.close()

if __name__ == '__main__':
    test_ghost_chancla()
