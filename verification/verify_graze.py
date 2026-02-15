
from playwright.sync_api import sync_playwright
import time
import os

def run_test():
    # 1. Read original file
    with open('chancla_bomb.html', 'r') as f:
        content = f.read()

    # 2. Inject debug hooks
    # Find a good injection point. After variable declarations seems safe.
    injection_point = "let chanclas = [];"
    injection_code = """
            let chanclas = [];
            window.debug = {
                getScore: () => score,
                getPlayer: () => player,
                getChanclas: () => chanclas,
                setChanclas: (c) => chanclas = c,
                setPlayerX: (x) => player.x = x,
                resetScore: () => score = 0
            };
    """
    new_content = content.replace(injection_point, injection_code)

    test_file = 'chancla_bomb_test.html'
    with open(test_file, 'w') as f:
        f.write(new_content)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            cwd = os.getcwd()
            page.goto('file://' + cwd + '/' + test_file)

            # Start game
            page.locator('#game').click()
            time.sleep(1) # Wait for init

            # Setup scenario
            # Player at center (200), y=630 (700-70).
            # Spawn chancla at x=255 (dx=55).
            # Graze dist < 75. Hit dist approx 43.
            # So 55 is perfect for graze.

            # Also ensure chancla is not 'slapped' and moves down.
            setup_script = """
                const p = window.debug.getPlayer();
                window.debug.setPlayerX(200);
                window.debug.resetScore();

                // Clear existing chanclas
                window.debug.setChanclas([]);

                // Add test chancla
                // y needs to be close enough to graze but not hit yet?
                // Or just place it above and let it fall.
                // Player y is 630.
                // Place chancla at y = 550, falling down.
                const c = {
                    x: 255,
                    y: 550,
                    vx: 0,
                    vy: 100, // Slow fall
                    w: 32,
                    h: 18,
                    type: 'normal',
                    rotation: 0,
                    rotSpeed: 0,
                    slapped: false,
                    grazed: false // Important: init as false
                };
                window.debug.setChanclas([c]);
            """
            page.evaluate(setup_script)

            # Wait for chancla to pass player
            # Distance 80px (630-550). Speed 100px/s.
            # Should take 0.8s to reach player y.
            # Graze check happens every frame.
            time.sleep(1.5)

            # Check score
            final_score = page.evaluate("window.debug.getScore()")
            print(f"Final Score: {final_score}")

            if final_score >= 15:
                print("SUCCESS: Graze detected!")
            else:
                print("FAILURE: No graze detected.")

            browser.close()
    finally:
        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)

if __name__ == '__main__':
    run_test()
