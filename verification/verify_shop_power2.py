from playwright.sync_api import sync_playwright
import os
import glob

def run_cuj(page):
    file_url = f"file://{os.path.abspath('index.html')}"
    page.goto(file_url)
    page.wait_for_timeout(500)

    # Click on shop button (Shop / Tienda is the second button, center roughly at y=500 in my previous screenshot it looks to be between 450 and 520)
    page.mouse.click(200, 500)
    page.wait_for_timeout(500)

    # Take screenshot at the shop
    page.screenshot(path="/home/jules/verification/screenshots/verification2.png")
    page.wait_for_timeout(1000)

if __name__ == "__main__":
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
