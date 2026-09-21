from playwright.sync_api import sync_playwright
import os

def test_game_start():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        errors = []
        page.on("pageerror", lambda err: errors.append(err.message))

        page.goto(f"file://{os.path.abspath('index.html')}")

        # Click Play button
        page.mouse.click(100, 450)

        page.wait_for_timeout(2000)

        # Click Play button in chancla_bomb.html
        page.goto(f"file://{os.path.abspath('chancla_bomb.html')}")
        page.mouse.click(100, 450)

        page.wait_for_timeout(2000)

        browser.close()

        if errors:
            print(f"Errors found: {errors}")
            assert False, "JavaScript errors detected"
        else:
            print("No errors found.")

if __name__ == "__main__":
    test_game_start()
