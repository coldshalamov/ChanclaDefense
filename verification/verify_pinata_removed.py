from playwright.sync_api import sync_playwright
import os
import glob
import time

def run_cuj(page):
    url = f"file://{os.path.abspath('index.html')}"
    page.goto(url)
    page.wait_for_timeout(500)

    # Fast forward internal state for testing if possible
    # We can inject JS to simulate pinata spawn logic, if it still existed.
    # However since we removed the logic entirely, we'll just show the game runs fine.

    # Start game
    page.mouse.click(200, 400)
    page.wait_for_timeout(1000)

    # Let the game play for a bit
    for _ in range(3):
        # Click to slap periodically
        page.mouse.click(200, 200)
        page.wait_for_timeout(1000)

    # Take screenshot at the key moment
    os.makedirs("/home/jules/verification/screenshots", exist_ok=True)
    page.screenshot(path="/home/jules/verification/screenshots/verification.png")
    page.wait_for_timeout(1000)

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        os.makedirs("/home/jules/verification/videos", exist_ok=True)
        # Clean up old videos
        for f in glob.glob("/home/jules/verification/videos/*.webm"):
            os.remove(f)

        context = browser.new_context(
            record_video_dir="/home/jules/verification/videos"
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()
            browser.close()

        videos = glob.glob("/home/jules/verification/videos/*.webm")
        if videos:
            print(f"Video saved to: {videos[0]}")
        else:
            print("Failed to save video.")
