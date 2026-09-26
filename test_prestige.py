from playwright.sync_api import sync_playwright
import os

def test_prestige_ui():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"file://{os.path.abspath('index.html')}")

        page.evaluate('''
            localStorage.setItem('chancla_bomb_save', JSON.stringify({
                stats: {wins: 11},
                prestigeTokens: 5,
                prestige: 1
            }));
            location.reload();
        ''')
        page.wait_for_timeout(500)

        # Dispatch click via JS directly to canvas with relative coordinates
        page.evaluate('''
            const evt = new MouseEvent('click', {
                clientX: document.querySelector('canvas').getBoundingClientRect().left + 205 + 155/2,
                clientY: document.querySelector('canvas').getBoundingClientRect().top + 610 + 46/2
            });
            document.querySelector('canvas').dispatchEvent(evt);
        ''')

        page.wait_for_timeout(500)
        os.makedirs('/home/jules/verification/screenshots', exist_ok=True)
        page.screenshot(path='/home/jules/verification/screenshots/prestige_shop.png')

        browser.close()

if __name__ == '__main__':
    test_prestige_ui()
