from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(record_video_dir="verification/")
        page = context.new_page()

        cwd = os.getcwd()
        page.goto(f'file://{cwd}/index.html')
        page.wait_for_timeout(500)

        # Trigger game start
        page.keyboard.press('Enter')
        page.wait_for_timeout(500)

        # We need to hack the win state for verification.
        # We can run an evaluate script to trigger the win condition immediately.
        page.evaluate('''() => {
            // Give 3 wins so we can see the math: 50 + (3 * 50) = 200 bonus
            const data = JSON.parse(localStorage.getItem('chancla_bomb_save') || '{}');
            if(!data.stats) data.stats = {};
            data.stats.wins = 3;
            localStorage.setItem('chancla_bomb_save', JSON.stringify(data));

            // Reload and restart to apply wins
            location.reload();
        }''')

        page.wait_for_timeout(500)
        page.keyboard.press('Enter')
        page.wait_for_timeout(500)

        # Trigger win
        page.evaluate('''() => {
            // Need to set anger to 0 to trigger the win
            // But we can't directly access the IIFE scope.
            // We'll dispatch a bunch of perfect hits or we can just rewrite the script tag.
        }''')

        # A simpler way is to just click the Boss level text to verify that first.
        page.screenshot(path='verification/boss_level.png')

        # Close context to save video
        context.close()
        browser.close()

if __name__ == '__main__':
    run()
