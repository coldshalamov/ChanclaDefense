from playwright.sync_api import sync_playwright
import os
import glob
import time

def run_cuj(page):
    file_url = f"file://{os.path.abspath('index.html')}"
    page.goto(file_url)
    page.wait_for_timeout(500)

    # Bypass IIFE to inject enough coins to buy everything
    # But Playwright can't easily do it for index.html as gameData is local to the closure.
    # Instead, we will simulate the user clicking on shop, and just take a screenshot of the shop to prove Slap Power is there.

    # The title screen has a shop button at y=470
    # Let's click it to enter the shop
    page.mouse.click(200, 470)
    page.wait_for_timeout(500)

    # Take screenshot at the shop
    page.screenshot(path="/home/jules/verification/screenshots/verification.png")
    page.wait_for_timeout(1000)

if __name__ == "__main__":
    os.makedirs("/home/jules/verification/videos", exist_ok=True)
    os.makedirs("/home/jules/verification/screenshots", exist_ok=True)

    # clean old videos
    for f in glob.glob("/home/jules/verification/videos/*.webm"):
        os.remove(f)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="/home/jules/verification/videos",
            viewport={"width": 400, "height": 700}
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()
            browser.close()
