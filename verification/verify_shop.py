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

        # Click Shop Button (col2=205, row1=430) -> center x=205+155/2=282.5, y=430+46/2=453
        page.evaluate("""
            const canvas = document.getElementById('game');
            const rect = canvas.getBoundingClientRect();
            const clickEvent = new MouseEvent('click', {
                clientX: rect.left + 282 * (rect.width / canvas.width),
                clientY: rect.top + 453 * (rect.height / canvas.height)
            });
            canvas.dispatchEvent(clickEvent);
        """)

        time.sleep(0.5)
        page.screenshot(path="verification/shop_initial.png")

        # Click greed upgrade (6th item, y=140+5*80 = 540) -> center y=540+70/2 = 575
        page.evaluate("""
            const canvas = document.getElementById('game');
            const rect = canvas.getBoundingClientRect();
            const clickEvent = new MouseEvent('click', {
                clientX: rect.left + 225 * (rect.width / canvas.width),
                clientY: rect.top + 575 * (rect.height / canvas.height)
            });
            canvas.dispatchEvent(clickEvent);
        """)

        time.sleep(0.5)

        # Screenshot of shop after purchases
        page.screenshot(path="verification/shop_purchased.png")

        browser.close()

if __name__ == "__main__":
    run()
