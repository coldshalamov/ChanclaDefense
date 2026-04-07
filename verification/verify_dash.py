import time
from playwright.sync_api import sync_playwright

def test_dash(page):
    page.goto(f"file:///app/index.html")

    page.evaluate("""
        () => {
            const scripts = document.querySelectorAll('script');
            let content = scripts[scripts.length - 1].textContent;
            content = content.replace('let state = STATE.TITLE;', 'let state = STATE.PLAYING; window.state = state;');
            content = content.replace('const player = {', 'window.player = {');
            content = content.replace('let dashTimer = 0;', 'window.dashTimerObj = {get val() { return dashTimer; }}; let dashTimer = 0;');
            content = content.replace('})();', '})();');
            const newScript = document.createElement('script');
            newScript.textContent = content;
            document.body.appendChild(newScript);
        }
    """)
    page.wait_for_timeout(500)

    # Need a small trick: hitTimer decreases every frame.
    # We want to catch it right after the double tap.

    # Send a quick double tap
    page.keyboard.press('ArrowRight')
    page.wait_for_timeout(50)
    page.keyboard.press('ArrowRight')

    # Small wait to let 1-2 frames pass
    page.wait_for_timeout(50)

    # Read the state
    hit_timer = page.evaluate('window.player.hitTimer')
    print(f"Hit Timer right after double tap: {hit_timer}")

    page.screenshot(path="/app/verification/dash_verification.png")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            test_dash(page)
        except Exception as e:
            print("Error during test:", e)
        finally:
            browser.close()
