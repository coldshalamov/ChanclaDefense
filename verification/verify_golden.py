from playwright.sync_api import sync_playwright
import os
import re

def run_cuj(page):
    # Modify the HTML to mock state and force a golden chancla
    with open('index.html', 'r') as f:
        content = f.read()

    # Expose state
    content = content.replace('(() => {', 'window.gameApp = (() => {')
    content = content.replace('})();', 'return { getGameData: () => gameData, getState: () => state, setState: (s) => { state = s; }, chanclas: chanclas }; })();')

    # Mock golden chancla spawn logic to 100%
    content = content.replace('const isGolden = !isBomb && !isHoming && !isSuper && !isFire && Math.random() < 0.05;', 'const isGolden = true;')

    with open('temp_golden_test.html', 'w') as f:
        f.write(content)

    filepath = f"file://{os.path.abspath('temp_golden_test.html')}"
    page.goto(filepath)
    page.wait_for_timeout(500)

    # Start game
    page.keyboard.press('Enter')
    page.wait_for_timeout(1000)

    # Wait for the golden chancla to fall a bit
    page.wait_for_timeout(1000)

    # Take screenshot of it falling
    page.screenshot(path="/home/jules/verification/screenshots/golden_falling.png")

    # Press space to slap it
    page.keyboard.press('Space')
    page.wait_for_timeout(500)

    # Take screenshot of the slap effect
    page.screenshot(path="/home/jules/verification/screenshots/golden_slap.png")
    page.wait_for_timeout(1000)

if __name__ == "__main__":
    os.makedirs("/home/jules/verification/videos", exist_ok=True)
    os.makedirs("/home/jules/verification/screenshots", exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="/home/jules/verification/videos",
            viewport={"width": 800, "height": 600}
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()
            browser.close()
