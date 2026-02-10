from playwright.sync_api import sync_playwright
import time
import os

def run():
    print("Starting game loop verification...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        cwd = os.getcwd()
        page.goto(f'file://{cwd}/index.html')

        # Click to start the game
        print("Clicking canvas to start game...")
        page.click('#game')

        # Run for 10 seconds
        print("Running for 10 seconds...")
        time.sleep(10)

        # Check if the page is still alive (no crash/error navigation)
        title = page.title()
        print(f"Page title after 10s: {title}")
        assert title == "Chancla Bomb: Isa vs. Su Gringo Para Siempre"

        # Take a screenshot to confirm it's rendering
        page.screenshot(path='verification/game_loop_success.png')
        print("Screenshot saved to verification/game_loop_success.png")

        browser.close()
    print("Verification complete.")

if __name__ == '__main__':
    run()
