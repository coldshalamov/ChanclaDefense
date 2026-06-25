from playwright.sync_api import sync_playwright
import time
import os

def run_cuj(page):
    cwd = os.getcwd()
    page.goto(f'file://{cwd}/index.html')
    page.wait_for_timeout(500)

    # Click play to start
    page.click('#game')
    page.wait_for_timeout(1000)

    # Wait for a projectile and try to hit it
    # For testing purposes, we'll wait a bit and just press space multiple times to simulate slaps
    for _ in range(15):
        page.keyboard.press('Space')
        page.wait_for_timeout(300)

    # Take screenshot at the key moment (hopefully after some damage)
    page.screenshot(path="/home/jules/verification/screenshots/verification.png")
    page.wait_for_timeout(1000)  # Hold final state for the video

if __name__ == "__main__":
    os.makedirs('/home/jules/verification/videos', exist_ok=True)
    os.makedirs('/home/jules/verification/screenshots', exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="/home/jules/verification/videos"
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()  # MUST close context to save the video
            browser.close()
