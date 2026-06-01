from playwright.sync_api import sync_playwright
import os
import glob
import re

def run_cuj(page):
    # To reliably enter shop, bypass IIFE and set state directly
    with open('index.html', 'r') as f:
        content = f.read()

    # Strip IIFE wrapper
    content = re.sub(r'^\s*\(\(\)\s*=>\s*\{\s*', '', content, flags=re.MULTILINE)
    content = re.sub(r'\}\)\(\);\s*$', '', content)

    # Expose state
    content = content.replace("let state = STATE.TITLE;", "window.state = STATE.SHOP;")

    with open('verification/temp_test.html', 'w') as f:
        f.write(content)

    file_url = f"file://{os.path.abspath('verification/temp_test.html')}"
    page.goto(file_url)
    page.wait_for_timeout(500)

    page.screenshot(path="/home/jules/verification/screenshots/verification3.png")
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
