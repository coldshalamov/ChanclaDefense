import os
import time
from playwright.sync_api import sync_playwright

def run_verification():
    # Read original file
    with open("chancla_bomb.html", "r") as f:
        content = f.read()

    # Inject debug hook to force rage mode
    injection = """
            window.debug_forceRage = () => {
                state = STATE.PLAYING;
                resetGame();
                isa.anger = 40; // Below 50%
                // Set time so super chanclas can spawn in spread
                timeElapsed = 20;
                superEnabled = true;
                // Wait for one update tick to trigger rage mode and spread attack
            };
            initTitle();
    """
    parts = content.rsplit("initTitle();", 1)
    modified_content = parts[0] + injection + parts[1]

    temp_file = "verification/test_rage.html"
    with open(temp_file, "w") as f:
        f.write(modified_content)

    file_path = os.path.abspath(temp_file)
    file_url = f"file://{file_path}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 450, "height": 800})
        page.goto(file_url)

        # Wait for canvas
        page.wait_for_selector("canvas")

        # Trigger rage mode
        page.evaluate("window.debug_forceRage()")

        # Wait for a few frames for the update loop to process and trigger spread attack + visual changes
        page.wait_for_timeout(1500)

        # Screenshot
        output_path = "verification/rage_verification.png"
        page.screenshot(path=output_path)
        print(f"Screenshot saved to {output_path}")

        browser.close()

if __name__ == "__main__":
    run_verification()
