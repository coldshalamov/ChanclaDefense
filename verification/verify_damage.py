from playwright.sync_api import sync_playwright
import time
import os
import re

def verify_damage():
    # We will modify a copy of the index to test damage specifically
    with open('index.html', 'r') as f:
        content = f.read()

    # Expose the game app
    content = re.sub(r'^\s*\(\(\)\s*=>\s*\{', 'window.gameApp = (() => {', content, flags=re.MULTILINE)
    content = re.sub(r'\}\)\(\);\s*$', 'return { startGameFromTitle, state: () => state, STATE, spawnChancla, chanclas: () => chanclas }; })();', content, flags=re.MULTILINE)

    with open('verification/index_test_damage.html', 'w') as f:
        f.write(content)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Record video just in case
        context = browser.new_context(record_video_dir='/app/verification/videos')
        page = context.new_page()

        page.goto(f"file://{os.path.abspath('verification/index_test_damage.html')}")

        # Start game
        page.evaluate("window.gameApp.startGameFromTitle()")
        time.sleep(0.5)

        # Spawn a chancla directly on the boss to cause damage instantly, or just call deal damage logic
        page.evaluate("""
            let c = window.gameApp.chanclas();
            window.gameApp.spawnChancla();
            let allC = window.gameApp.chanclas();
            if (allC.length > 0) {
                // Force a hit on Isa
                let projectile = allC[0];
                projectile.x = 200;
                projectile.y = 70; // Isa's y position
                projectile.slapped = true;
                projectile.type = 'bomb';
            }
        """)

        time.sleep(0.1) # Wait for update loop to process collision
        page.screenshot(path='/app/verification/damage_numbers.png')

        context.close()
        browser.close()

if __name__ == "__main__":
    verify_damage()
