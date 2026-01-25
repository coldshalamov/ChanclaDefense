import os
import time
from playwright.sync_api import sync_playwright

def verify_miss_feedback():
    # 1. Prepare the HTML with injected code to expose internals
    with open("chancla_bomb.html", "r", encoding="utf-8") as f:
        content = f.read()

    # Inject code to expose rosePetals via a getter to handle reassignment in resetGame
    injected_content = content.replace(
        "})();",
        "window.getRosePetals = () => rosePetals; window.trySlap = trySlap; window.chanclas = chanclas; window.resetGame = resetGame; })();"
    )

    temp_file = "verification/temp_miss_test.html"
    with open(temp_file, "w", encoding="utf-8") as f:
        f.write(injected_content)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            cwd = os.getcwd()
            file_path = f"file://{cwd}/{temp_file}"
            page.goto(file_path)

            # Wait for canvas
            page.locator("#game").wait_for()

            # Start the game
            page.evaluate("window.resetGame()")

            # Wait for any fades
            time.sleep(0.5)

            # Clear chanclas to ensure we miss
            page.evaluate("window.chanclas.length = 0")

            # Trigger slap (which should be a miss)
            page.evaluate("window.trySlap()")

            # Wait a tiny bit for the frame to render
            time.sleep(0.05)

            # Check rosePetals for the "dash" emoji
            petals = page.evaluate("window.getRosePetals()")

            found = False
            for p in petals:
                if p.get('emoji') == '💨':
                    found = True
                    break

            # Take screenshot
            screenshot_path = "verification/miss_slap.png"
            page.screenshot(path=screenshot_path)
            print(f"Screenshot saved to {screenshot_path}")

            if found:
                print("SUCCESS: Found '💨' emoji in rosePetals after missed slap.")
            else:
                print("FAILURE: Did not find '💨' emoji in rosePetals after missed slap.")
                emojis = [p.get('emoji') for p in petals if p.get('emoji')]
                print(f"Found emojis: {emojis}")

            browser.close()

            if not found:
                exit(1)

    finally:
        # Cleanup
        if os.path.exists(temp_file):
            os.remove(temp_file)

if __name__ == "__main__":
    verify_miss_feedback()
