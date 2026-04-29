import os
import time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load index.html
        abs_path = os.path.abspath('index.html')
        page.goto('file://' + abs_path)

        # Wait a moment for canvas to render
        page.wait_for_timeout(1000)

        # Take screenshot of the title screen
        screenshot_path = 'verification/boss_level_title.png'
        page.screenshot(path=screenshot_path)
        print(f"Screenshot taken: {screenshot_path}")

        # Now simulate a win
        page.evaluate('''
            // Expose gameData temporarily if possible, or just modify localStorage and reload
            let save = localStorage.getItem('chancla_bomb_save');
            if (save) {
                save = JSON.parse(save);
            } else {
                save = { stats: { wins: 1 } };
            }
            save.stats.wins = 5;
            localStorage.setItem('chancla_bomb_save', JSON.stringify(save));
        ''')

        # Reload to apply save
        page.reload()
        page.wait_for_timeout(1000)

        screenshot_path_2 = 'verification/boss_level_title_5.png'
        page.screenshot(path=screenshot_path_2)
        print(f"Screenshot taken: {screenshot_path_2}")

        browser.close()

if __name__ == '__main__':
    run()
