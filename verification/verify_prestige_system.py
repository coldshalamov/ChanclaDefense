import re
import os
import shutil
from playwright.sync_api import sync_playwright

# 1) Clean up old htmls to avoid confusion
shutil.copyfile("index.html", "verification/index_temp.html")

with open("verification/index_temp.html", "r") as f:
    content = f.read()

# 2) Strip the IIFE wrapper
content = re.sub(r'^\s*\(\(.*=>\s*\{\s*', '', content, flags=re.MULTILINE)
content = re.sub(r'\}\)\(\);\s*$', '', content, flags=re.MULTILINE)

# 3) Convert 'let state =' to 'var state =' globally
content = re.sub(r'\blet\s+state\b', r'var state', content)

# 4) Overwrite the file with IIFE removed
with open("verification/index_temp.html", "w") as f:
    f.write(content)

def run_cuj(page):
    # Navigate to our patched file
    page.goto('file://' + os.path.abspath('verification/index_temp.html'))
    page.wait_for_timeout(500)

    # Force the condition to show the Prestige button (10 wins)
    page.evaluate("() => { gameData.stats.wins = 10; saveGameData(); state = STATE.TITLE; }")
    page.wait_for_timeout(500)

    # Re-draw the title screen so it re-checks wins
    page.evaluate("() => { state = STATE.TITLE; }")
    page.wait_for_timeout(500)

    # Click the Prestige button on the Title Screen
    page.mouse.click(200, 640)
    page.wait_for_timeout(1000)

    # We should now be on the PRESTIGE screen
    # Screenshot the Prestige Screen
    page.screenshot(path="/home/jules/verification/screenshots/verification.png")
    page.wait_for_timeout(500)

    # Click the "Prestige Now" button
    page.mouse.click(200, 330)
    page.wait_for_timeout(1000)

    # We should be back on the TITLE screen now.
    # Take a screenshot to show we are back on title
    page.screenshot(path="/home/jules/verification/screenshots/verification_post.png")
    page.wait_for_timeout(1000)

if __name__ == "__main__":
    os.makedirs("/home/jules/verification/videos", exist_ok=True)
    os.makedirs("/home/jules/verification/screenshots", exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="/home/jules/verification/videos"
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()
            browser.close()
