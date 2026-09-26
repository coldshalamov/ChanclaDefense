from playwright.sync_api import sync_playwright
import os

def test_prestige_ui():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"file://{os.path.abspath('index.html')}")

        # Need to extract gameData and localstorage interaction out since it's IIFE
        # Let's just click around from a fresh start since we can't eval local scope
        page.evaluate('''
            localStorage.setItem('chancla_bomb_save', JSON.stringify({
                stats: {wins: 11},
                prestigeTokens: 5
            }));
            location.reload();
        ''')
        page.wait_for_timeout(500)

        # Click Prestige button
        page.mouse.click(205 + 155/2, 610 + 46/2)
        page.wait_for_timeout(500)

        # Take screenshot of prestige screen
        os.makedirs('/home/jules/verification/screenshots', exist_ok=True)
        page.screenshot(path='/home/jules/verification/screenshots/prestige.png')

        browser.close()

if __name__ == '__main__':
    test_prestige_ui()
