from playwright.sync_api import sync_playwright
import time
import os
import re

def create_mocked_html():
    with open('index.html', 'r') as f:
        content = f.read()

    # Modify the gameData to simulate a returning player and a streak
    old_date = 'new Date(new Date().setDate(new Date().getDate() - 1)).toDateString()'

    # We will inject a custom init script right after gameData is declared
    injection = f"""
            try {{
                gameData.lastLogin = {old_date};
                gameData.loginStreak = 2;
                gameData.stats.wins = 15; // To show prestige button too
                saveGameData();
            }} catch(e) {{}}
"""

    # Let's replace the gameData init block to inject our mock
    search = "if (!gameData.loginStreak) gameData.loginStreak = 0;"
    replace = search + injection

    content = content.replace(search, replace)

    with open('verification/mocked_index.html', 'w') as f:
        f.write(content)


def run_cuj(page):
    # Load the local HTML file (mocked version)
    page.goto(f"file://{os.path.abspath('verification/mocked_index.html')}")
    page.wait_for_timeout(1000)

    # Take screenshot at the key moment, the daily reward message should be displayed
    page.screenshot(path="/home/jules/verification/screenshots/daily_reward.png")
    page.wait_for_timeout(2000)  # Hold final state for the video

if __name__ == "__main__":
    create_mocked_html()
    os.makedirs("/home/jules/verification/screenshots", exist_ok=True)
    os.makedirs("/home/jules/verification/videos", exist_ok=True)
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
