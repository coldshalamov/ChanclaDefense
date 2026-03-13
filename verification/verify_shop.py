from playwright.sync_api import sync_playwright
import os

def test_shop(page):
    filepath = 'file://' + os.path.abspath('index.html')

    # Configure viewport and touch
    page.set_viewport_size({'width': 450, 'height': 800})

    # Init save data
    init_script = """
    localStorage.setItem('chancla_bomb_save', JSON.stringify({
        coins: 1000,
        upgrades: { lives: 0, shield: 0, cooldown: 0, speed: 0 },
        bestScore: 0
    }));
    """
    page.add_init_script(init_script)
    page.goto(filepath)

    page.wait_for_timeout(500)

    # Inject click via evaluate to bypass touch scaling
    page.evaluate('''
        const canvas = document.getElementById('game');
        const rect = canvas.getBoundingClientRect();
        const scaleY = rect.height / canvas.height;
        const scaleX = rect.width / canvas.width;

        const targetX = rect.left + (canvas.width / 2) * scaleX;
        const targetY = rect.top + (475) * scaleY;

        const ev = new MouseEvent('click', {
            clientX: targetX,
            clientY: targetY,
            bubbles: true
        });
        canvas.dispatchEvent(ev);
    ''')

    page.wait_for_timeout(500)

    # Take screenshot of the new shop UI
    page.screenshot(path="verification/shop.png")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(has_touch=True, is_mobile=True)
        page = context.new_page()
        try:
            test_shop(page)
        finally:
            browser.close()
