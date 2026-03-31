import os
from playwright.sync_api import sync_playwright

def run_cuj(page):
    with open('index.html', 'r') as f:
        content = f.read()

    # Expose state to window
    modified_content = content.replace(
        "let state = STATE.TITLE;",
        "let state = STATE.TITLE; window.setState = (s) => state = s;"
    )

    modified_content = modified_content.replace(
        "let gameData = { coins: 0, upgrades: { lives: 0, shield: 0, cooldown: 0, speed: 0 }, bestScore: 0, stats: { totalSlaps: 0, perfectSlaps: 0, gamesPlayed: 0, totalCoinsEarned: 0 }, achievements: {}, cosmetics: [], currentHat: null };",
        "let gameData = { coins: 1000, upgrades: { lives: 0, shield: 0, cooldown: 0, speed: 0 }, bestScore: 0, stats: { totalSlaps: 0, perfectSlaps: 0, gamesPlayed: 0, totalCoinsEarned: 0 }, achievements: {}, cosmetics: [], currentHat: null }; window.gameData = gameData;"
    )

    with open('index_test.html', 'w') as f:
        f.write(modified_content)

    test_url = 'file://' + os.path.abspath('index_test.html')
    page.goto(test_url)
    page.wait_for_timeout(500)

    # Hide directions
    page.evaluate("document.body.classList.add('hide-directions')")
    page.wait_for_timeout(500)

    # 1. Title Screen Screenshot
    page.screenshot(path="verification/screenshots/cosmetics_01_title.png")

    # 2. Go to Cosmetics
    page.evaluate("window.setState('cosmetics')")
    page.wait_for_timeout(500)
    page.screenshot(path="verification/screenshots/cosmetics_02_menu.png")

    # 3. Buy and equip crown
    page.evaluate("window.gameData.cosmetics.push('crown'); window.gameData.currentHat = 'crown'; window.gameData.coins -= 500;")
    page.wait_for_timeout(500)
    page.screenshot(path="verification/screenshots/cosmetics_03_bought.png")

    # 4. Show in-game
    page.evaluate("window.setState('playing')")
    page.wait_for_timeout(500)
    page.screenshot(path="verification/screenshots/cosmetics_04_ingame.png")
    page.wait_for_timeout(1000)

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="verification/videos",
            viewport={'width': 400, 'height': 700},
            is_mobile=True,
            has_touch=True
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()
            browser.close()

    if os.path.exists('index_test.html'):
        os.remove('index_test.html')
