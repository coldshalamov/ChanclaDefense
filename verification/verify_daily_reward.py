from playwright.sync_api import sync_playwright
import os

def run_cuj(page):
    # Load index.html with file protocol
    page.goto(f"file://{os.path.abspath('index.html')}")
    page.wait_for_timeout(1000)

    # We should see the daily reward message on the title screen for 5 seconds
    page.screenshot(path="/home/jules/verification/screenshots/daily_reward.png")
    page.wait_for_timeout(1000)

    # To test logic we would ideally inject localStorage state before loading,
    # but the default behavior on first load will hit checkDailyReward()
    # and gameData.lastLogin is null, triggering the streak = 1 and 50 coins reward.
    page.wait_for_timeout(4000)

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
