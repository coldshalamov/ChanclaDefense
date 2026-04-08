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

        # Inject our state hack by modifying the script and appending it
        page.evaluate('''() => {
            const data = { coins: 0, upgrades: { lives: 0, shield: 0, cooldown: 0, speed: 0 }, bestScore: 0, stats: { totalSlaps: 0, perfectSlaps: 0, gamesPlayed: 0, totalCoinsEarned: 0, wins: 3 }, achievements: {}, cosmetics: ['none'], currentHat: 'none' };
            localStorage.setItem('chancla_bomb_save', JSON.stringify(data));
            location.reload();
        }''')
        page.wait_for_timeout(500)
        page.screenshot(path='verification/boss_level_title.png')

        # Start game
        page.keyboard.press('Enter')
        page.wait_for_timeout(500)

        # To win, we need to extract the script and expose triggerWin or just modify isa.anger.
        # But we can also just expose it from the source string.
        script_content = page.evaluate('() => document.scripts[0].innerText')
        modified_script = script_content.replace('function triggerWin() {', 'window.triggerWin = function() {')

        page.evaluate(f'''() => {{
            const script = document.createElement('script');
            script.innerHTML = `{modified_script}`;
            document.body.appendChild(script);
        }}''')

        page.wait_for_timeout(500)
        page.evaluate('window.triggerWin()')
        page.wait_for_timeout(1500)

        page.screenshot(path='verification/win_screen_bonus.png')

        context.close()
        browser.close()

if __name__ == '__main__':
    run()
