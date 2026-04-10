from playwright.sync_api import sync_playwright
import time
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        cwd = os.path.dirname(os.getcwd())
        page.goto(f'file://{cwd}/index.html')

        # We inject wins to see the title screen update
        page.evaluate("""
            const saved = localStorage.getItem('chancla_bomb_save') ? JSON.parse(localStorage.getItem('chancla_bomb_save')) : {};
            if (!saved.stats) saved.stats = { totalSlaps: 0, perfectSlaps: 0, gamesPlayed: 0, totalCoinsEarned: 0, wins: 0 };
            saved.stats.wins = 5;
            localStorage.setItem('chancla_bomb_save', JSON.stringify(saved));
        """)
        # reload to apply
        page.reload()

        time.sleep(1)
        page.screenshot(path='title_screen_wins_ui.png')
        browser.close()

if __name__ == '__main__':
    run()
