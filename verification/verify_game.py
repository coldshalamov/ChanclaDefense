from playwright.sync_api import sync_playwright
import os
import glob

def run_cuj(page):
    page.goto(f"file://{os.path.abspath('index.html')}")
    page.wait_for_timeout(1000)

    # Click the canvas to start the game
    page.mouse.click(500, 500)
    page.wait_for_timeout(1000)

    # We want to see some game play
    page.keyboard.press('Enter')
    page.wait_for_timeout(1000)

    # Just survive a bit
    for _ in range(5):
        page.keyboard.press('Space')
        page.wait_for_timeout(1000)

    page.screenshot(path="/app/verification/screenshots/verification.png")
    page.wait_for_timeout(1000)

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="/app/verification/videos"
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()
            browser.close()

    # get video path
    video_path = glob.glob("/app/verification/videos/*.webm")[0]
    print(f"Video saved to {video_path}")
