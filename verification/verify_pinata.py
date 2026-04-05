from playwright.sync_api import sync_playwright
import os
import time

def verify_pinata():
    with sync_playwright() as p:
        # Match the mobile configuration used in other verification scripts
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 414, 'height': 896},
            is_mobile=True,
            has_touch=True
        )
        page = context.new_page()

        # Load the local file
        current_dir = os.getcwd()
        page.goto(f'file://{current_dir}/index.html')

        # Start game
        page.keyboard.press('Enter')
        time.sleep(0.5)

        # Inject a pinata specifically and ensure no chanclas are active to prevent death
        page.evaluate("""() => {
            chanclas = []; // Clear chanclas
            if (typeof pinatas !== 'undefined') {
                pinatas.push({ x: 200, y: 100, vy: 0, w: 40, h: 40, hits: 0, rotation: 0, rotSpeed: 0 });
            }
        }""")

        # Wait a tiny bit for render
        time.sleep(0.1)

        # Take screenshot of pinata on screen
        page.screenshot(path='verification/pinata_spawn.png')

        # Slap it twice
        page.keyboard.press(' ')
        time.sleep(0.1)
        page.keyboard.press(' ')
        time.sleep(0.1)

        page.screenshot(path='verification/pinata_juggle.png')

        # Third slap - triggers confetti
        page.keyboard.press(' ')
        time.sleep(0.1)

        page.screenshot(path='verification/pinata_explosion.png')

        browser.close()

if __name__ == '__main__':
    verify_pinata()
