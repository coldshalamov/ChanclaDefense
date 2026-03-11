from playwright.sync_api import sync_playwright
import time
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 450, 'height': 800}) # approximate mobile size
        page = context.new_page()

        cwd = os.getcwd()
        page.goto(f"file://{cwd}/index.html")

        # Wait for canvas
        page.wait_for_selector("#game")

        # Give player 1000 coins to buy things via local storage and reload
        page.evaluate("localStorage.setItem('chancla_bomb_save', JSON.stringify({ coins: 1000, upgrades: { lives: 0, shield: 0, cooldown: 0, speed: 0 }, bestScore: 0 }));")
        page.reload()
        page.wait_for_selector("#game")

        # Let's dynamically inject a click trigger using page.evaluate logic on the canvas
        page.evaluate("""
        () => {
            const canvas = document.getElementById('game');
            const rect = canvas.getBoundingClientRect();

            // Go to shop
            const evtShop = new MouseEvent('click', {
                clientX: rect.left + (rect.width * 200 / 400),
                clientY: rect.top + (rect.height * 473 / 700)
            });
            canvas.dispatchEvent(evtShop);
        }
        """)

        time.sleep(1)

        page.screenshot(path="verification/shop_verification.png")

        # Simulate buying the fourth item (speed)
        # speed is at 160 + 3*100 = 460. Button height 80. Center 500.
        page.evaluate("""
        () => {
            const canvas = document.getElementById('game');
            const rect = canvas.getBoundingClientRect();

            const evtBuy = new MouseEvent('click', {
                clientX: rect.left + (rect.width * 200 / 400),
                clientY: rect.top + (rect.height * 500 / 700)
            });
            canvas.dispatchEvent(evtBuy);
        }
        """)

        time.sleep(0.5)

        # Click buy speed again
        page.evaluate("""
        () => {
            const canvas = document.getElementById('game');
            const rect = canvas.getBoundingClientRect();

            const evtBuy = new MouseEvent('click', {
                clientX: rect.left + (rect.width * 200 / 400),
                clientY: rect.top + (rect.height * 500 / 700)
            });
            canvas.dispatchEvent(evtBuy);
        }
        """)

        time.sleep(0.5)

        page.screenshot(path="verification/shop_after_buy.png")

        browser.close()

if __name__ == "__main__":
    run()
