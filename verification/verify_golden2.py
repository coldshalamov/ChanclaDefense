from playwright.sync_api import sync_playwright
import os

def run_cuj(page):
    # Modify the HTML to mock state and force a golden chancla
    with open('index.html', 'r') as f:
        content = f.read()

    # Expose state
    content = content.replace('(() => {', 'window.gameApp = (() => {')
    content = content.replace('})();', 'return { getGameData: () => gameData, getState: () => state, setState: (s) => { state = s; }, chanclas: chanclas, player: player, score: score }; })();')

    # Mock golden chancla spawn logic to 100%
    content = content.replace('const isGolden = !isBomb && !isHoming && !isSuper && !isFire && Math.random() < 0.05;', 'const isGolden = true;')

    # Slow down time
    content = content.replace('let dt = Math.min((ts - lastTime) / 1000, 0.1);', 'let dt = Math.min((ts - lastTime) / 1000, 0.1) * 0.1;')

    with open('temp_golden_test.html', 'w') as f:
        f.write(content)

    filepath = f"file://{os.path.abspath('temp_golden_test.html')}"
    page.goto(filepath)
    page.wait_for_timeout(500)

    # Start game
    page.keyboard.press('Enter')
    page.wait_for_timeout(500)

    # Wait until chancla reaches player height and space is pressed to slap
    for _ in range(30):
        page.wait_for_timeout(200)
        chanclas = page.evaluate('window.gameApp.chanclas')
        player = page.evaluate('window.gameApp.player')
        if chanclas:
            c = chanclas[0]
            if c['y'] > player['y'] - 50:
                break

    page.keyboard.press('Space')
    page.wait_for_timeout(1000)

    page.screenshot(path="/home/jules/verification/screenshots/golden_slap2.png")

if __name__ == "__main__":
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
