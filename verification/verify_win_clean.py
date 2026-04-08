from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(record_video_dir="verification/")
        page = context.new_page()

        cwd = os.getcwd()
        # Read file directly
        with open(os.path.join(cwd, 'index.html'), 'r') as f:
            content = f.read()

        # Modify content to expose triggerWin and gameData, and replace localstorage
        content = content.replace('function triggerWin() {', 'window.triggerWin = function() {')
        content = content.replace('let gameData = {', 'window.gameData = {')
        content = content.replace('localStorage.getItem', '(() => null)')
        content = content.replace('localStorage.setItem', '(() => null)')

        page.set_content(content)
        page.wait_for_timeout(500)

        # Set wins and redraw
        page.evaluate('''() => {
            window.gameData.stats.wins = 3;
        }''')
        page.keyboard.press('Enter') # Start game
        page.wait_for_timeout(200)
        page.keyboard.press('Enter') # Back to title screen
        page.wait_for_timeout(500)

        page.screenshot(path='verification/boss_level_title.png')

        page.keyboard.press('Enter') # Start game again
        page.wait_for_timeout(500)
        page.evaluate('window.triggerWin()')
        page.wait_for_timeout(1500)

        page.screenshot(path='verification/win_screen_bonus.png')

        context.close()
        browser.close()

if __name__ == '__main__':
    run()
