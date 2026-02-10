import os
import sys
from playwright.sync_api import sync_playwright

def verify_graze():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Capture console logs
        page.on("console", lambda msg: print(f"CONSOLE: {msg.text}"))

        # Load the game
        file_path = os.path.abspath("chancla_bomb.html")
        url = f"file://{file_path}"
        print(f"Loading: {url}")
        page.goto(url)

        # Wait for game internals
        page.wait_for_function("() => window.gameInternals")
        print("Game internals found.")

        # Run test logic
        result = page.evaluate("""() => {
            const game = window.gameInternals;

            // Start game to ensure state is PLAYING
            game.resetGame();

            const p = game.player;

            // Setup Scenario
            p.x = 200;
            p.y = 600;
            game.chanclas.length = 0;

            game.spawnChancla();
            const c = game.chanclas[0];

            // Graze position
            c.x = p.x + 60;
            c.y = p.y;
            c.vx = 0;
            c.vy = 0;
            c.grazed = false;
            c.slapped = false;

            const startScore = game.score;

            // Update
            game.update(0.016);

            return {
                startScore,
                finalScore: game.score,
                isGrazed: c.grazed,
                hasGrazeText: game.floatTexts.some(t => t.text.includes('GRAZE'))
            };
        }""")

        print(f"Result: {result}")

        if result['isGrazed'] and result['finalScore'] == result['startScore'] + 15 and result['hasGrazeText']:
            print("SUCCESS: Graze mechanic verified!")
        else:
            print("FAILURE: Graze mechanic failed.")
            sys.exit(1)

        browser.close()

if __name__ == "__main__":
    verify_graze()
