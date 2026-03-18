import os
import time
from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    # Expose game internal state and bypass overlay
    init_script = """
        const testData = {
            coins: 50,
            upgrades: { lives: 0, shield: 0, cooldown: 0, speed: 0 },
            bestScore: 160,
            stats: { totalSlaps: 5, perfectSlaps: 0, gamesPlayed: 2, totalCoinsEarned: 50 },
            achievements: {}
        };
        localStorage.setItem('chancla_bomb_save', JSON.stringify(testData));
    """
    page.add_init_script(init_script)

    file_url = f"file://{os.path.abspath('index.html')}"
    page.goto(file_url)
    page.wait_for_timeout(1000)

    # Dispatch synthetic mouse events to bypass touch zone overlays
    # achievements button: center (200, 500) internally
    page.evaluate("""() => {
        const c = document.getElementById('game');
        const rect = c.getBoundingClientRect();
        // Calculate offset back from internal scale
        const scaleX = c.width / rect.width;
        const scaleY = c.height / rect.height;
        const cx = rect.left + 200 / scaleX;
        const cy = rect.top + 500 / scaleY;
        const e = new MouseEvent('click', { clientX: cx, clientY: cy, bubbles: true });
        c.dispatchEvent(e);
    }""")

    page.wait_for_timeout(1000)
    page.screenshot(path="verification/achievements_canvas_click.png")

    # Claim High Roller achievement: center internally approx (200, 480)
    page.evaluate("""() => {
        const c = document.getElementById('game');
        const rect = c.getBoundingClientRect();
        const scaleX = c.width / rect.width;
        const scaleY = c.height / rect.height;
        const cx = rect.left + 200 / scaleX;
        const cy = rect.top + 480 / scaleY;
        const e = new MouseEvent('click', { clientX: cx, clientY: cy, bubbles: true });
        c.dispatchEvent(e);
    }""")

    page.wait_for_timeout(1000)
    page.screenshot(path="verification/achievements_claimed.png")

    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
