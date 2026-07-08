from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Record video to see dynamic journey
        context = browser.new_context(
            record_video_dir='/app/verification/videos',
            viewport={'width': 400, 'height': 700}
        )
        page = context.new_page()

        # Load local index.html
        file_path = f"file://{os.path.abspath('index.html')}"
        page.goto(file_path)

        # Inject gameData state for testing (10 wins unlocked prestige)
        page.evaluate("""() => {
            const data = {
                coins: 500,
                upgrades: { lives: 0, shield: 0, cooldown: 0, speed: 0, power: 0 },
                bestScore: 0,
                stats: { totalSlaps: 0, perfectSlaps: 0, gamesPlayed: 0, totalCoinsEarned: 0, wins: 10 },
                achievements: {},
                cosmetics: ['none'],
                currentHat: 'none',
                prestige: 1
            };
            localStorage.setItem('chancla_bomb_save', JSON.stringify(data));
        }""")

        # Reload to apply state
        page.reload()
        page.wait_for_timeout(500)

        # Screenshot Title Screen with Prestige Button
        page.screenshot(path='/app/verification/prestige_title.png')
        print("Prestige title screen screenshot taken.")

        # Click Prestige button
        page.locator('canvas#game').click(position={'x': 200, 'y': 643}, force=True)
        page.wait_for_timeout(500)

        # Screenshot Prestige Screen
        page.screenshot(path='/app/verification/prestige_screen.png')
        print("Prestige screen screenshot taken.")

        # Click confirm
        page.locator('canvas#game').click(position={'x': 200, 'y': 430}, force=True)
        page.wait_for_timeout(500)

        page.screenshot(path='/app/verification/prestige_confirmed.png')
        print("Prestige confirmed screenshot taken.")

        context.close()
        browser.close()

if __name__ == '__main__':
    run()
