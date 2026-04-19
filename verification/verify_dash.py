import os
import glob
from playwright.sync_api import sync_playwright

def run_cuj(page):
    abs_path = os.path.abspath('index.html')
    page.goto(f"file://{abs_path}")
    page.wait_for_timeout(500)

    # Press Enter to start
    page.keyboard.press('Enter')
    page.wait_for_timeout(500)

    # Perform a double tap on the 'A' key to dash left
    page.keyboard.press('a')
    page.keyboard.press('a')

    # Wait a tiny bit to capture the dash visual trail
    page.wait_for_timeout(50)

    page.screenshot(path="verification/screenshots/dash.png")
    page.wait_for_timeout(1000)

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="verification/videos"
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()
            browser.close()

    # Find the newly created video file and rename it
    video_files = glob.glob("verification/videos/*.webm")
    if video_files:
        latest_video = max(video_files, key=os.path.getctime)
        os.rename(latest_video, "verification/videos/dash.webm")
