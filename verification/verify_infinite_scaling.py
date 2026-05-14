import os
from playwright.sync_api import sync_playwright
import time

def verify_scaling(page):
    # Navigate to index.html using an absolute file path
    index_path = os.path.abspath('index.html')
    page.goto(f'file://{index_path}')

    # Wait for the page to load
    page.wait_for_timeout(1000)

    # Simulate having won 5 times by modifying localStorage and reloading
    page.evaluate("""
        const saved = JSON.parse(localStorage.getItem('chancla_bomb_save') || '{}');
        if (!saved.stats) saved.stats = {};
        saved.stats.wins = 6;
        localStorage.setItem('chancla_bomb_save', JSON.stringify(saved));
    """)
    page.reload()
    page.wait_for_timeout(1000)

    # Take screenshot of the title screen showing "Boss Level: 6"
    page.screenshot(path="verification/scaling_title_screen.png")
    print("Screenshot saved to verification/scaling_title_screen.png")

    # Start the game
    page.keyboard.press("Enter")
    page.wait_for_timeout(1000)

    # Expose game state, trigger win
    page.evaluate("""
        const scripts = document.querySelectorAll('script');
        const lastScript = scripts[scripts.length - 1];
        let content = lastScript.textContent;
        content = content.replace('const isa = {', 'window.isa = {');
        content = content.replace('state = STATE.TITLE;', 'state = STATE.TITLE; window.triggerWin = triggerWin;');

        const newScript = document.createElement('script');
        newScript.textContent = content;
        document.body.appendChild(newScript);
    """)
    page.wait_for_timeout(500)

    page.evaluate("window.triggerWin();")
    page.wait_for_timeout(1000)

    # Take a screenshot of the win screen showing defeated level and bonus coins
    page.screenshot(path="verification/scaling_win_screen.png")
    print("Screenshot saved to verification/scaling_win_screen.png")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        try:
            verify_scaling(page)
        except Exception as e:
            print(f"Error during verification: {e}")
        finally:
            browser.close()
