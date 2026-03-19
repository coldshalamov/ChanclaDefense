from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Mobile viewport for this game
        context = browser.new_context(
            viewport={'width': 450, 'height': 800},
            has_touch=True,
            is_mobile=True,
            record_video_dir="verification/video"
        )
        page = context.new_page()

        # Load the local HTML file
        file_path = f"file://{os.getcwd()}/index.html"
        page.goto(file_path)
        page.wait_for_timeout(500)

        # Click Play button (from center)
        page.mouse.click(200, 400)
        page.wait_for_timeout(500)

        # We need to wait a little for the game to spawn chanclas
        # The first chancla spawns around 1.2s.
        page.wait_for_timeout(1500)

        # Take a screenshot to see the new sprite
        page.screenshot(path="verification/verification.png")

        # Wait a bit more to see more gameplay
        page.wait_for_timeout(1000)

        # Ensure context is closed to save video
        context.close()
        browser.close()

if __name__ == "__main__":
    os.makedirs("verification/video", exist_ok=True)
    run()
