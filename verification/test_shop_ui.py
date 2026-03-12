from playwright.sync_api import sync_playwright
import time
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 450, 'height': 800}) # approximate mobile size
        page = context.new_page()

        # Give 500 coins directly to localStorage BEFORE load
        page.add_init_script("window.localStorage.setItem('chancla_bomb_save', JSON.stringify({ coins: 500, upgrades: { lives: 1, shield: 0, cooldown: 5, speed: 2 }, bestScore: 0 }))")

        cwd = os.getcwd()
        page.goto(f"file://{cwd}/index.html")

        # Wait for canvas
        page.wait_for_selector("#game")

        # Inject code to force state to shop
        page.evaluate('''() => {
            const scripts = document.querySelectorAll('script');
            let content = scripts[scripts.length - 1].textContent;

            content = content.replace('let state = STATE.TITLE;', 'let state = STATE.SHOP;');

            scripts[scripts.length - 1].remove();
            const newScript = document.createElement('script');
            newScript.textContent = content;
            document.body.appendChild(newScript);
        }''')

        time.sleep(1)
        page.screenshot(path="verification/shop_ui_verification.png")

        # Click maxed out item (cooldown - 3rd item, y=160+200=360)
        box = page.locator("#game").bounding_box()
        page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] * (400 / 700))
        time.sleep(1)

        # Click buy item (speed - 4th item, y=160+300=460)
        page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] * (500 / 700))
        time.sleep(1)
        page.screenshot(path="verification/shop_ui_purchased.png")

        browser.close()

if __name__ == "__main__":
    run()
