
import os
from playwright.sync_api import sync_playwright

def create_test_file():
    with open('index.html', 'r') as f:
        content = f.read()

    # Inject exposure code
    exposure_code = """
            window.game = {
                player: player,
                getChanclas: () => chanclas,
                getScore: () => score,
                getSpecialBar: () => specialAttackBar,
                spawnChancla: spawnChancla,
                update: update,
                resetGame: resetGame
            };
    """
    # Insert before the last line which is likely })();
    new_content = content.replace('initTitle();', 'initTitle();' + exposure_code)

    with open('chancla_bomb_test.html', 'w') as f:
        f.write(new_content)

def verify_graze():
    create_test_file()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        cwd = os.getcwd()
        page.goto('file://' + cwd + '/chancla_bomb_test.html')

        # Start game
        page.evaluate("window.game.resetGame()")

        # Setup scenario: Player at 200, 600 (w=55, h=45). Chancla at 260, 600 (distance 60).
        # Graze dist is 75. Hit dist overlap is ~40-50.

        # Initial score
        score_start = page.evaluate("window.game.getScore()")
        print(f"Start Score: {score_start}")

        # Spawn chancla manually
        page.evaluate("""
            const c = { x: 260, y: 600, vx: 0, vy: 0, w: 32, h: 18, type: 'normal', rotation: 0, rotSpeed: 0, grazed: false, slapped: false };
            window.game.getChanclas().push(c);
        """)

        # Update frame
        page.evaluate("window.game.update(0.1)")

        # Check score
        score_end = page.evaluate("window.game.getScore()")
        print(f"End Score: {score_end}")

        try:
            chancla_grazed = page.evaluate("window.game.getChanclas()[0].grazed")
            print(f"Chancla Grazed: {chancla_grazed}")
        except:
            chancla_grazed = False
            print("Chancla Grazed: False (property missing?)")

        if score_end == score_start + 15:
            print("SUCCESS: Graze mechanic works!")
        else:
            print("FAILURE: Graze mechanic not working (Score unchanged).")

        browser.close()

if __name__ == "__main__":
    verify_graze()
