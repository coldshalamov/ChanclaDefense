import re
import os
import shutil
from playwright.sync_api import sync_playwright

with open("verification/index_temp.html", "r") as f:
    content = f.read()

def run_cuj(page):
    page.goto('file://' + os.path.abspath('verification/index_temp.html'))
    page.wait_for_timeout(500)

    # Force PRESTIGE state
    page.evaluate("() => { gameData.stats.wins = 10; saveGameData(); state = STATE.PRESTIGE; }")
    page.wait_for_timeout(500)

    page.screenshot(path="/home/jules/verification/screenshots/verification2.png")
    page.wait_for_timeout(500)

if __name__ == "__main__":
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
