from playwright.sync_api import sync_playwright
import time
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 450, 'height': 800}, has_touch=True, is_mobile=True)
        page = context.new_page()

        cwd = os.getcwd()
        page.goto(f"file://{cwd}/index.html")

        # Give it 1000 coins to buy stuff
        page.evaluate("localStorage.setItem('chancla_bomb_save', JSON.stringify({ coins: 1000, upgrades: {}, bestScore: 0 }))")
        page.reload()

        page.wait_for_selector("#game")

        # Click Shop Button (110, 450, w, 46) -> center is around x=225, y=473
        page.evaluate("""
            const canvas = document.getElementById('game');
            const rect = canvas.getBoundingClientRect();
            const clickEvent = new MouseEvent('click', {
                clientX: rect.left + 225 * (rect.width / canvas.width),
                clientY: rect.top + 473 * (rect.height / canvas.height)
            });
            canvas.dispatchEvent(clickEvent);
        """)

        time.sleep(0.5)

        # Screenshot of empty shop
        page.screenshot(path="verification/shop_initial.png")

        # Click first upgrade (Extra Life) - pos: y=160 to 240, x=40 to 410 -> center x=225, y=200
        page.evaluate("""
            const canvas = document.getElementById('game');
            const rect = canvas.getBoundingClientRect();
            const clickEvent = new MouseEvent('click', {
                clientX: rect.left + 225 * (rect.width / canvas.width),
                clientY: rect.top + 200 * (rect.height / canvas.height)
            });
            canvas.dispatchEvent(clickEvent);
        """)

        time.sleep(0.5)

        # Click third upgrade (Cooldown) - pos: y=360 to 440 -> center x=225, y=400
        page.evaluate("""
            const canvas = document.getElementById('game');
            const rect = canvas.getBoundingClientRect();
            const clickEvent = new MouseEvent('click', {
                clientX: rect.left + 225 * (rect.width / canvas.width),
                clientY: rect.top + 400 * (rect.height / canvas.height)
            });
            canvas.dispatchEvent(clickEvent);
        """)

        time.sleep(0.5)

        # Screenshot of shop after purchases
        page.screenshot(path="verification/shop_purchased.png")

        browser.close()

if __name__ == "__main__":
    run()
