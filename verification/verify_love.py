import os
from playwright.sync_api import sync_playwright

def run_verification():
    # Read original file
    with open("chancla_bomb.html", "r") as f:
        content = f.read()

    # Inject debug hook
    # We replace the call to initTitle() at the end of the script
    # with code that exposes a global function to force the state and spawn a heart
    injection = """
            window.debug_spawnHeart = () => {
                state = STATE.PLAYING;
                // Reset to ensure clean state
                resetGame();
                // Spawn heart directly on player
                spawnPowerup('heart', player.x, player.y);
            };
            initTitle();
    """
    # Replace the LAST occurrence of initTitle(); just to be safe, though there is likely only one call at the end
    parts = content.rsplit("initTitle();", 1)
    modified_content = parts[0] + injection + parts[1]

    # Write temp file
    temp_file = "verification/test_love.html"
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

        # Trigger heart spawn
        page.evaluate("window.debug_spawnHeart()")

        # Wait for a few frames for the update loop to process collision and set state
        page.wait_for_timeout(500)

        # Screenshot
        output_path = "verification/love_verification.png"
        page.screenshot(path=output_path)
        print(f"Screenshot saved to {output_path}")

        browser.close()

if __name__ == "__main__":
    run_verification()
