import os
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Using a much larger viewport to avoid responsive scaling throwing off absolute coords
        context = browser.new_context(viewport={'width': 800, 'height': 800})
        page = context.new_page()

        init_script = """
        localStorage.setItem('chancla_bomb_save', JSON.stringify({
            coins: 50000,
            upgrades: { lives: 4, shield: 4, cooldown: 4, speed: 9 },
            bestScore: 0
        }));
        """
        page.add_init_script(init_script)

        page.goto(f"file://{os.getcwd()}/index.html")
        page.wait_for_selector("#game")

        # Wait for fonts/rendering
        page.wait_for_timeout(1000)

        # Send clicks directly by evaluating JS to bypass complex bounding box mappings
        # The internal logic handles scaling from canvas client coordinates

        def js_click(x, y):
            print(f"JS click at canvas internal {x}, {y}")
            page.evaluate(f'''() => {{
                const canvas = document.getElementById('game');
                const rect = canvas.getBoundingClientRect();
                const scaleX = canvas.width / rect.width;
                const scaleY = canvas.height / rect.height;

                const clientX = rect.left + ({x} / scaleX);
                const clientY = rect.top + ({y} / scaleY);

                const event = new MouseEvent('click', {{
                    view: window,
                    bubbles: true,
                    cancelable: true,
                    clientX: clientX,
                    clientY: clientY
                }});
                canvas.dispatchEvent(event);
            }}''')
            page.wait_for_timeout(500)

        # Shop button: cy = 350. Button is y: 440 to 486.
        js_click(200, 460)

        page.screenshot(path="verification/shop_before_max.png")

        # Upgrade buttons (x=200, y = 180 + 90*i + 25)
        js_click(200, 205) # Lives
        js_click(200, 295) # Shield
        js_click(200, 385) # Cooldown
        js_click(200, 475) # Speed

        page.screenshot(path="verification/shop_maxed.png")

        # Back button
        js_click(200, 620)

        # Play button
        js_click(200, 400)

        page.wait_for_timeout(500)
        page.screenshot(path="verification/game_maxed_upgrades.png")

        browser.close()

if __name__ == "__main__":
    run()
