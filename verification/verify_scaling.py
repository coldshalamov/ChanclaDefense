import os
import math
from playwright.sync_api import sync_playwright

def test_scaling_ui(page):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_url = f"file://{os.path.dirname(current_dir)}/index.html"

    # 1. Start with 0 wins
    page.goto(file_url)

    # Wait for canvas to be ready
    page.wait_for_selector('canvas#game')
    page.wait_for_timeout(500)

    page.screenshot(path=f"{current_dir}/scaling_0_wins.png")

    # 2. Inject some wins and refresh
    wins = 3
    js_code = f"""
    let saved = localStorage.getItem('chancla_bomb_save');
    let data = saved ? JSON.parse(saved) : {{}};
    if (!data.stats) data.stats = {{}};
    data.stats.wins = {wins};
    localStorage.setItem('chancla_bomb_save', JSON.stringify(data));
    """
    page.evaluate(js_code)

    page.reload()
    page.wait_for_timeout(500)
    page.screenshot(path=f"{current_dir}/scaling_{wins}_wins.png")

    # 3. Start the game and verify the enraged state threshold and win bonus
    page.keyboard.press('Enter') # Start game
    page.wait_for_timeout(500)
    page.screenshot(path=f"{current_dir}/scaling_game_start_{wins}_wins.png")

    # Trigger win
    page.evaluate("if(typeof triggerWin === 'function') { triggerWin(); }")
    page.wait_for_timeout(1000)
    page.screenshot(path=f"{current_dir}/scaling_win_screen_{wins}_wins.png")


if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            test_scaling_ui(page)
            print("Verification script ran successfully.")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()
