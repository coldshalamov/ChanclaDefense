import os
import re
from playwright.sync_api import sync_playwright

def run():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # The title screen is blocking clicks due to overlay, so let's directly modify the initial state
    content = content.replace(
        'let state = STATE.TITLE;',
        'let state = STATE.PLAYING;'
    )

    injected_logic = """
                if (!window.injected) {
                    window.injected = true;
                    spawnChancla();
                    chanclas[0].x = 200;
                    chanclas[0].y = 350;
                    chanclas[0].vx = 0;
                    chanclas[0].vy = 0;
                    player.x = 200;
                    player.y = 450;
                }

                if (window.doSlapNow) {
                    window.doSlapNow = false;
                    player.x = 200;
                    player.y = 350;
                    trySlap();
                }
"""
    content = content.replace('if (state !== STATE.PLAYING) return;', 'if (state !== STATE.PLAYING) return;' + injected_logic)

    # Force a golden chancla to spawn and bypass random chance
    content = content.replace(
        'const isGolden = !isBomb && !isHoming && !isSuper && !isFire && Math.random() < 0.02;',
        'const isGolden = true;'
    )
    content = content.replace(
        'const isBomb = Math.random() < 0.08;',
        'const isBomb = false;'
    )
    # prevent continuous spawning
    content = content.replace(
        'if (spawnTimer >= spawnInterval) {',
        'if (false) {'
    )

    with open('verification/test_golden.html', 'w', encoding='utf-8') as f:
        f.write(content)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_viewport_size({"width": 400, "height": 700})

        file_url = "file://" + os.path.abspath("verification/test_golden.html")
        page.goto(file_url)
        page.wait_for_timeout(500)

        # We are now in PLAYING state and the injected logic has frozen the golden chancla in the middle
        page.screenshot(path="verification/golden_chancla.png")
        print("Screenshot taken: verification/golden_chancla.png")

        # Force a perfect slap
        page.evaluate("() => { window.doSlapNow = true; }")
        page.wait_for_timeout(100) # wait a tiny bit for impact/text

        page.screenshot(path="verification/golden_slap.png")
        print("Screenshot taken: verification/golden_slap.png")

        browser.close()

if __name__ == "__main__":
    run()
