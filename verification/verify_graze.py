import os
import time
import shutil
from playwright.sync_api import sync_playwright

def verify_graze():
    cwd = os.getcwd()
    original_file = f"{cwd}/chancla_bomb.html"
    test_file = f"{cwd}/test_chancla_bomb.html"

    # Read original file
    with open(original_file, 'r') as f:
        content = f.read()

    # Inject code to expose variables
    # We'll inject it right after the IIFE starts or variables are declared.
    # Looking for: "const keys = { left: false, right: false };"
    # This is near the end of declarations.
    injection_marker = "const keys = { left: false, right: false };"
    injection_code = """
            const keys = { left: false, right: false };
            window.game = {
                player: player,
                getChanclas: () => chanclas,
                getScore: () => score,
                getFloatTexts: () => floatTexts,
                resetGame: resetGame,
                update: update
            };
    """

    if injection_marker not in content:
        print("Error: Could not find injection marker in chancla_bomb.html")
        return False

    modified_content = content.replace(injection_marker, injection_code)

    with open(test_file, 'w') as f:
        f.write(modified_content)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(f"file://{test_file}")

            # Start game
            print("Starting game...")
            page.evaluate("window.game.resetGame()")
            time.sleep(0.5) # Wait for fade in/start

            # Get initial score
            initial_score = page.evaluate("window.game.getScore()")
            print(f"Initial Score: {initial_score}")

            # Inject chancla for graze
            # Player is at x=200, y=630 (default)
            # Inject at x=260 (dist 60), y=630. Graze range < 75. Hit range > 40.
            print("Injecting chancla...")
            page.evaluate("""
                window.game.getChanclas().push({
                    x: window.game.player.x + 60,
                    y: window.game.player.y,
                    vx: 0, vy: 0,
                    w: 32, h: 18,
                    type: 'normal',
                    rotation: 0, rotSpeed: 0,
                    grazed: false
                });
            """)

            # Wait for update loop to process
            time.sleep(0.2)

            # Force update to ensure logic runs in headless env if RAF is throttled
            page.evaluate("window.game.update(0.1)")

            # Debug
            chancla_state = page.evaluate("window.game.getChanclas()[0]")
            print(f"Chancla[0]: {chancla_state}")

            # Check results
            final_score = page.evaluate("window.game.getScore()")
            has_graze_text = page.evaluate("""
                window.game.getFloatTexts().some(t => t.text.includes('GRAZE'))
            """)

            print(f"Final Score: {final_score}")
            print(f"Has Graze Text: {has_graze_text}")

            if final_score > initial_score and has_graze_text:
                print("SUCCESS: Graze mechanic verified!")
                result = True
            else:
                print("FAILURE: Graze mechanic not working.")
                result = False

            browser.close()
            return result

    except Exception as e:
        print(f"Error during verification: {e}")
        return False
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)

if __name__ == "__main__":
    if verify_graze():
        exit(0)
    else:
        exit(1)
