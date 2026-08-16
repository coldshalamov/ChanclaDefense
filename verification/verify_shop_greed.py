from playwright.sync_api import sync_playwright
import time
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="/home/jules/verification/videos",
            viewport={'width': 450, 'height': 800},
            has_touch=True,
            is_mobile=True
        )
        page = context.new_page()

        cwd = os.getcwd()
        page.goto(f"file://{cwd}/index.html")

        # Give it 5000 coins to buy stuff
        page.evaluate("localStorage.setItem('chancla_bomb_save', JSON.stringify({ coins: 5000, upgrades: {}, bestScore: 0 }))")
        page.reload()

        page.wait_for_selector("#game")

        # We need to dispatch events exactly like verify_shop.js
        # The Shop button on Title Screen: col2 = 205, row1 = 430. Center = x: 282.5, y: 453
        page.evaluate("""
            const canvas = document.getElementById('game');
            const rect = canvas.getBoundingClientRect();
            const clickEvent = new MouseEvent('click', {
                clientX: rect.left + 282.5 * (rect.width / canvas.width),
                clientY: rect.top + 453 * (rect.height / canvas.height)
            });
            canvas.dispatchEvent(clickEvent);
        """)

        time.sleep(1)

        # Screenshot of shop initial state with Greed
        page.screenshot(path="/home/jules/verification/screenshots/shop_before_greed.png")

        # Greed upgrade center: 140 + 5*80 + 35 = 575. Center x = 200
        for _ in range(5):
            page.evaluate("""
                const canvas = document.getElementById('game');
                const rect = canvas.getBoundingClientRect();
                const clickEvent = new MouseEvent('click', {
                    clientX: rect.left + 200 * (rect.width / canvas.width),
                    clientY: rect.top + 575 * (rect.height / canvas.height)
                });
                canvas.dispatchEvent(clickEvent);
            """)
            time.sleep(0.5)

        # Screenshot of shop after purchases
        page.screenshot(path="/home/jules/verification/screenshots/shop_after_greed.png")
        time.sleep(1)

        # Check localStorage
        saved = page.evaluate("JSON.parse(localStorage.getItem('chancla_bomb_save'))")
        print(f"Saved Data: {saved}")

        # Click back button to trigger title
        page.evaluate("""
            const canvas = document.getElementById('game');
            const rect = canvas.getBoundingClientRect();
            const clickEvent = new MouseEvent('click', {
                clientX: rect.left + 200 * (rect.width / canvas.width),
                clientY: rect.top + 655 * (rect.height / canvas.height)
            });
            canvas.dispatchEvent(clickEvent);
        """)
        time.sleep(1)

        context.close()
        browser.close()

if __name__ == "__main__":
    run()
