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

        # Inject our state hack
        content = page.content()
        # Expose state and gameData
        content = content.replace('let state = STATE.TITLE;', 'let state = STATE.TITLE; window.state = state; window.STATE = STATE;')
        content = content.replace('let gameData = {', 'window.gameData = {')
        content = content.replace('function triggerWin() {', 'window.triggerWin = function() {')

        page.set_content(content)
        page.wait_for_timeout(500)

        # Trigger title screen with hacked wins
        page.evaluate('''() => {
            window.gameData.stats.wins = 2; // Level 3
            drawTitleScreen(); // Force redraw
        }''')
        page.wait_for_timeout(500)
        page.screenshot(path='verification/boss_level.png')

        # Trigger win screen
        page.evaluate('''() => {
            window.triggerWin();
        }''')
        page.wait_for_timeout(1500) # Wait for animation
        page.screenshot(path='verification/win_bonus.png')

        context.close()
        browser.close()

if __name__ == '__main__':
    run()
