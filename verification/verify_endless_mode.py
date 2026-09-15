from playwright.sync_api import sync_playwright
import time
import os
import glob

def run_cuj(page):
    cwd = os.getcwd()
    page.goto(f'file://{cwd}/index.html')
    page.wait_for_timeout(500)

    # Click Endless button (approx coordinates: x = col2 + btnW/2, y = row1 + btnH/2)
    # col2 = 205, btnW = 155 -> x = 205 + 77.5 = 282.5
    # row1 = 430, btnH = 46 -> y = 430 + 23 = 453
    page.mouse.click(282, 453)
    page.wait_for_timeout(2000)

    # Just wait out the game
    page.wait_for_timeout(10000)

    # Take screenshot at the key moment
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
    video_files = glob.glob('/app/verification/videos/*.webm')
    if video_files:
        print(f"Video saved to {video_files[0]}")
