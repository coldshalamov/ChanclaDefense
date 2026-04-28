import os
from playwright.sync_api import sync_playwright

def run_cuj(page):
    abs_path = os.path.abspath('index.html')
    # Because of IIFE, we extract, modify and inject
    with open('index.html', 'r') as f:
        html_content = f.read()

    # Expose state logic
    modified_html = html_content.replace('function endGame() {', 'window.isa = isa; window.triggerWin = triggerWin; function endGame() {')

    with open('temp_test.html', 'w') as f:
        f.write(modified_html)

    abs_temp_path = os.path.abspath('temp_test.html')

    page.goto(f"file://{abs_temp_path}")
    page.wait_for_timeout(500)

    page.evaluate('''
        const data = {
            coins: 0,
            upgrades: { lives: 0, shield: 0, cooldown: 0, speed: 0 },
            bestScore: 0,
            stats: { totalSlaps: 0, perfectSlaps: 0, gamesPlayed: 0, totalCoinsEarned: 0, wins: 3 },
            achievements: {},
            cosmetics: ['none'],
            currentHat: 'none'
        };
        localStorage.setItem('chancla_bomb_save', JSON.stringify(data));
    ''')

    page.reload()
    page.wait_for_timeout(500)

    page.screenshot(path="/home/jules/verification/screenshots/boss_level_title.png")

    page.keyboard.press("Enter")
    page.wait_for_timeout(500)

    page.evaluate('''
        // Modify the state directly to trigger win using our new logic
        window.isa.anger = 0;
        window.triggerWin();
    ''')

    page.wait_for_timeout(2500) # Wait for win animation

    page.screenshot(path="/home/jules/verification/screenshots/boss_defeat_win.png")
    page.wait_for_timeout(1000)

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="/home/jules/verification/videos",
            viewport={'width': 400, 'height': 700}
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()
            browser.close()
            if os.path.exists('temp_test.html'):
                os.remove('temp_test.html')
