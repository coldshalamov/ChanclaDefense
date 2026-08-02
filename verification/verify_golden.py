import re
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(record_video_dir='/app/verification/videos')
        page = context.new_page()

        # Read index.html and modify it to force the golden chancla spawn logic and bypass IIFE
        with open('index.html', 'r') as f:
            content = f.read()

        # Expose IIFE for debugging state
        content = re.sub(r'^\s*\(\(.*=>\s*\{\s*', 'window.gameApp = (() => {', content, count=1, flags=re.MULTILINE)
        content = re.sub(r'\}\)\(\);\s*$', 'return { getGameData: () => gameData, getState: () => state, getChanclas: () => chanclas }; })();', content, flags=re.MULTILINE)

        # Force state to PLAYING immediately
        content = content.replace("let state = STATE.TITLE;", "let state = STATE.PLAYING;")

        # Increase golden chancla spawn chance to 100% for verification
        content = content.replace("const isGolden = Math.random() < 0.05;", "const isGolden = true;")

        with open('verification/temp_golden.html', 'w') as f:
            f.write(content)

        # Load the modified game
        page.goto('file:///app/verification/temp_golden.html')

        # Wait a moment for game loop to spawn chanclas
        page.wait_for_timeout(2000)

        # Take a screenshot to show the golden chancla
        page.screenshot(path='verification/golden_chancla_spawn.png')

        # Simulate slapping by pressing space
        page.keyboard.press('Space')

        # Wait for the slap effect and text
        page.wait_for_timeout(200)

        page.screenshot(path='verification/golden_chancla_slap.png')

        context.close()
        browser.close()

if __name__ == '__main__':
    run()
