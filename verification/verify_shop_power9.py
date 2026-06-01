from playwright.sync_api import sync_playwright
import os
import glob
import re
import time

def run_cuj(page):
    with open('index.html', 'r') as f:
        content = f.read()

    # We will strip the IIFE wrapper and convert let to var, then we can easily control it.
    content = re.sub(r'^\s*\(\(\)\s*=>\s*\{\s*', '', content, flags=re.MULTILINE)
    content = re.sub(r'\}\)\(\);\s*$', '', content)

    content = re.sub(r'\blet\s+(state|gameData)\b', r'var \1', content)

    # And we also need to mock localStorage to avoid SecurityError
    content = content.replace("const saved = localStorage.getItem('chancla_bomb_save');", "const saved = null;")

    with open('verification/temp_test5.html', 'w') as f:
        f.write(content)

    file_url = f"file://{os.path.abspath('verification/temp_test5.html')}"
    page.goto(file_url)
    page.wait_for_timeout(500)

    page.evaluate("window.state = 'shop'; window.gameData.coins = 9999;")
    page.wait_for_timeout(500)

    page.screenshot(path="/home/jules/verification/screenshots/verification11.png")

    # Click 5th button
    page.mouse.click(200, 120 + 95*4 + 40)
    page.wait_for_timeout(500)
    page.screenshot(path="/home/jules/verification/screenshots/verification12.png")

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
