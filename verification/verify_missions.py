import os
import re
from playwright.sync_api import sync_playwright

def prepare_html():
    with open('index.html', 'r') as f:
        content = f.read()
    # Let's replace the IIFE definition to expose window.gameApp
    content = content.replace('(() => {', 'window.gameApp = (() => {')
    content = content.replace('})();', 'return { getGameData: () => gameData, getState: () => state, setState: (s) => { state = s; } }; })();')
    with open('temp_test.html', 'w') as f:
        f.write(content)

def run_cuj(page):
    file_path = f"file://{os.path.abspath('temp_test.html')}"
    page.goto(file_path)
    page.wait_for_timeout(500)

    # Change state to missions
    page.evaluate("window.gameApp.setState('missions')")
    page.wait_for_timeout(500)

    page.screenshot(path="/home/jules/verification/screenshots/missions_screen.png")
    page.wait_for_timeout(1000)

    # Go back to title
    page.evaluate("window.gameApp.setState('title')")
    page.wait_for_timeout(500)

    page.screenshot(path="/home/jules/verification/screenshots/title_screen.png")
    page.wait_for_timeout(500)

    # Start the game
    page.keyboard.press("Enter")
    page.wait_for_timeout(1000)

    # Try to slap
    page.keyboard.press("Space")
    page.wait_for_timeout(500)

    # Check gameData
    missions = page.evaluate("window.gameApp.getGameData().missions")
    print("Missions after slap:", missions)

if __name__ == "__main__":
    prepare_html()
    os.makedirs("/home/jules/verification/screenshots", exist_ok=True)
    os.makedirs("/home/jules/verification/videos", exist_ok=True)
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

    os.remove('temp_test.html')
