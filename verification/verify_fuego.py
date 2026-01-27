import os
from playwright.sync_api import sync_playwright

def verify_fuego():
    # 1. Read the original game file
    with open("chancla_bomb.html", "r", encoding="utf-8") as f:
        content = f.read()

    # 2. Inject code to force high combo
    # We look for "comboCount = 0;" inside resetGame and change it to 10
    # Note: There are two "comboCount = 0;" in the file (one init, one resetGame).
    # Since we are modifying text, we might hit both or one.
    # The first one is "let comboCount = 0;"
    # The second one is "comboCount = 0;" inside resetGame.
    # Let's target the one inside resetGame more specifically if possible,
    # or just replace "comboCount = 0;" which appears in resetGame.

    modified_content = content.replace("comboCount = 0;", "comboCount = 10;")

    # 3. Write to a temporary file
    test_file_path = os.path.abspath("verification/test_fuego.html")
    with open(test_file_path, "w", encoding="utf-8") as f:
        f.write(modified_content)

    print(f"Created temporary test file at: {test_file_path}")

    # 4. Run Playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        url = f"file://{test_file_path}"
        print(f"Loading {url}...")
        page.goto(url)

        # Wait for canvas
        page.wait_for_selector("canvas#game")

        # Click to start game (state goes from TITLE to PLAYING)
        # The click handler in the game starts it.
        page.click("canvas#game")

        # Wait a bit for the update loop to run and spawn particles
        # At combo 10, particles should spawn immediately
        page.wait_for_timeout(1000)

        # Take screenshot
        screenshot_path = "verification/fuego_effect.png"
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

        browser.close()

if __name__ == "__main__":
    verify_fuego()
