from playwright.sync_api import sync_playwright
import time
import os

def run_cuj(page):
    html_path = os.path.abspath('index.html')
    # Because of local storage access issues in file:// schema, we inject initialization script

    # We can inject data into localstorage before the page scripts run
    page.add_init_script("""
        localStorage.setItem('chancla_bomb_save', JSON.stringify({
            coins: 5000,
            upgrades: { lives: 0, shield: 0, cooldown: 0, speed: 0 },
            bestScore: 0,
            stats: { totalSlaps: 0, perfectSlaps: 0, gamesPlayed: 0, totalCoinsEarned: 0 },
            achievements: {},
            cosmetics: ['none'],
            currentHat: 'none'
        }));
    """)
    page.goto(f"file://{html_path}")
    page.wait_for_timeout(500)

    # To click cosmetics button (y=560 to 606)
    page.evaluate('''
        () => {
            const canvas = document.querySelector('canvas');
            const rect = canvas.getBoundingClientRect();
            const clickX = rect.left + (rect.width / 2);
            const clickY = rect.top + (580 * (rect.height / canvas.height));

            const event = new MouseEvent('click', {
                clientX: clickX,
                clientY: clickY,
                bubbles: true
            });
            canvas.dispatchEvent(event);
        }
    ''')
    page.wait_for_timeout(1000)
    page.screenshot(path="/home/jules/verification/screenshots/cosmetics_menu.png")

    # Buy the crown (cost 500)
    # y = 140 for the list.
    # none (y=140), cap (y=225), cowboy (y=310), crown (y=395)
    page.evaluate('''
        () => {
            const canvas = document.querySelector('canvas');
            const rect = canvas.getBoundingClientRect();
            const clickX = rect.left + (rect.width / 2);
            const clickY = rect.top + (420 * (rect.height / canvas.height));

            const event = new MouseEvent('click', {
                clientX: clickX,
                clientY: clickY,
                bubbles: true
            });
            canvas.dispatchEvent(event);
        }
    ''')
    page.wait_for_timeout(1000)
    page.screenshot(path="/home/jules/verification/screenshots/cosmetics_crown_equipped.png")

    # Go back to title (button y = canvas.height - 80 = 700 - 80 = 620)
    page.evaluate('''
        () => {
            const canvas = document.querySelector('canvas');
            const rect = canvas.getBoundingClientRect();
            const clickX = rect.left + (rect.width / 2);
            const clickY = rect.top + (650 * (rect.height / canvas.height));

            const event = new MouseEvent('click', {
                clientX: clickX,
                clientY: clickY,
                bubbles: true
            });
            canvas.dispatchEvent(event);
        }
    ''')
    page.wait_for_timeout(1000)
    page.screenshot(path="/home/jules/verification/screenshots/title_with_crown.png")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="/home/jules/verification/videos"
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()
            browser.close()