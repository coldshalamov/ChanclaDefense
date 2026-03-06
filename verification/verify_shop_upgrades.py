from playwright.sync_api import sync_playwright
import time
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 450, 'height': 800}) # approximate mobile size
        page = context.new_page()

        # Intercept local storage to set coins before the game loads
        page.add_init_script("""
            localStorage.setItem('chancla_bomb_save', JSON.stringify({
                coins: 5000,
                upgrades: { lives: 0, shield: 0, cooldown: 0, speed: 0 },
                bestScore: 0
            }));
        """)

        cwd = os.getcwd()
        page.goto(f"file://{cwd}/index.html")

        # Wait for canvas
        page.wait_for_selector("#game")

        # Give the page a moment to render the title screen
        time.sleep(0.5)

        # Click the shop button on the title screen
        # The Shop button on the title screen is roughly at y=450-496
        # Need to use the page evaluation to trigger the click
        page.evaluate("""
            const canvas = document.getElementById('game');
            const rect = canvas.getBoundingClientRect();
            // Dispatch click event for shop button
            const ev = new MouseEvent('click', {
                clientX: rect.left + 200 * (rect.width/400),
                clientY: rect.top + 470 * (rect.height/700)
            });
            canvas.dispatchEvent(ev);
        """)

        time.sleep(0.5)

        # Take a screenshot of the initial shop state
        page.screenshot(path="verification/shop_initial.png")

        # Buy "Speed" upgrade 3 times
        # The Speed upgrade is the 4th one. y position: 460
        for _ in range(3):
            page.evaluate("""
                const canvas = document.getElementById('game');
                const rect = canvas.getBoundingClientRect();
                const ev = new MouseEvent('click', {
                    clientX: rect.left + 200 * (rect.width/400),
                    clientY: rect.top + 480 * (rect.height/700)
                });
                canvas.dispatchEvent(ev);
            """)
            time.sleep(0.2)

        # Buy "Shield" upgrade (max level 1)
        # y position: 260
        page.evaluate("""
            const canvas = document.getElementById('game');
            const rect = canvas.getBoundingClientRect();
            const ev = new MouseEvent('click', {
                clientX: rect.left + 200 * (rect.width/400),
                clientY: rect.top + 280 * (rect.height/700)
            });
            canvas.dispatchEvent(ev);
        """)
        time.sleep(0.2)

        # Take a screenshot of the shop after purchases
        page.screenshot(path="verification/shop_after_purchases.png")

        browser.close()

if __name__ == "__main__":
    run()
