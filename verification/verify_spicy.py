from playwright.sync_api import sync_playwright
import time
import os
import sys

def verify_spicy():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the game from the file directly using absolute path
        cwd = os.getcwd()
        page.goto('file://' + cwd + '/index.html')

        # Wait for game to load
        time.sleep(1)

        # Start game by clicking Play button
        # Canvas is 400x700. Play button is around y=400.
        page.locator('#game').click(position={'x': 200, 'y': 400})
        time.sleep(1)

        # Inject Spicy Mode
        print("Injecting Spicy Mode...")
        page.evaluate("window.gameInternals.player.chiliTimer = 5")

        # Wait a bit for fire particles to spawn
        time.sleep(0.5)

        # Take screenshot of Spicy Mode (Fire Aura + Expression)
        page.screenshot(path='verification/spicy_mode.png')
        print("Screenshot taken: verification/spicy_mode.png")

        # Spawn a chancla directly on the player
        print("Spawning chancla on player...")
        page.evaluate("""
            const p = window.gameInternals.player;
            window.gameInternals.chanclas.push({
                x: p.x,
                y: p.y,
                vx: 0,
                vy: 100,
                w: 32,
                h: 18,
                type: 'normal',
                rotation: 0,
                rotSpeed: 0,
                slapped: false
            });
        """)

        # Wait for update loop to process collision
        time.sleep(0.1)

        # Take screenshot of Reflection (Impact)
        page.screenshot(path='verification/spicy_reflect.png')
        print("Screenshot taken: verification/spicy_reflect.png")

        # Check state
        result = page.evaluate("""
            () => {
                const c = window.gameInternals.chanclas.find(x => x.slapped);
                const p = window.gameInternals.player;
                const lastC = window.gameInternals.chanclas[window.gameInternals.chanclas.length - 1];

                return {
                    chanclaCount: window.gameInternals.chanclas.length,
                    slapped: lastC ? lastC.slapped : false,
                    vy: lastC ? lastC.vy : 0,
                    lives: p.lives
                };
            }
        """)

        print(f"Test Result: {result}")

        # Verify
        if result['slapped'] == True and result['vy'] < 0 and result['lives'] == 3:
            print("SUCCESS: Spicy Mode reflection worked!")
        else:
            print("FAILURE: Spicy Mode reflection failed.")
            sys.exit(1)

        browser.close()

if __name__ == '__main__':
    verify_spicy()
