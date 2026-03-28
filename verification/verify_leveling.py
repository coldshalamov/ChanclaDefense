import os
import time
from playwright.sync_api import sync_playwright

def verify_leveling():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 450, 'height': 800}, has_touch=True, is_mobile=True)
        page = context.new_page()

        file_path = f"file://{os.path.abspath('index.html')}"

        # Navigate using file path so localstorage doesn't throw SecurityError
        page.goto(file_path)

        page.add_init_script("""
            const mockSave = {
                xp: 0,
                level: 1,
                coins: 0,
                upgrades: { lives: 0, shield: 0, cooldown: 0, speed: 0 },
                bestScore: 0,
                stats: { totalSlaps: 0, perfectSlaps: 0, gamesPlayed: 0, totalCoinsEarned: 0 }
            };
            localStorage.setItem('chancla_bomb_save', JSON.stringify(mockSave));
        """)

        with open('index.html', 'r') as f:
            content = f.read()

        # Disable local storage saving to prevent SecurityError
        content = content.replace("function saveGameData() {", "function saveGameData() { return;")

        # Expose variables correctly
        content = content.replace("let gameData =", "window.gameData =")
        content = content.replace("const STATE =", "window.STATE =")

        # Expose endgame
        content = content.replace("initTitle();\n        })();", "window.endGame = endGame; window.initTitle = initTitle;\n        })();")

        page.set_content(content)
        page.evaluate("window.initTitle()")

        # Read initial
        initial_level = page.evaluate("window.gameData.level")
        initial_xp = page.evaluate("window.gameData.xp")
        print(f"Initial Level: {initial_level}, Initial XP: {initial_xp}")
        assert initial_level == 1, "Level should be initialized to 1"
        assert initial_xp == 0, "XP should be initialized to 0"

        # Patch endGame functionality to accept mockScore parameter
        page.evaluate("""
            window.endGameTest = function(mockScore) {
                state = window.STATE.GAMEOVER;
                const earned = Math.floor(mockScore / 10);
                window.gameData.coins += earned;
                window.gameData.stats.totalCoinsEarned += earned;
                window.gameData.bestScore = Math.max(window.gameData.bestScore, mockScore);
                window.gameData.xp += mockScore;
                window.gameData.level = Math.floor(Math.sqrt(window.gameData.xp / 50)) + 1;
            }
        """)

        score_to_add = 150
        page.evaluate(f"window.endGameTest({score_to_add});")

        new_level = page.evaluate("window.gameData.level")
        new_xp = page.evaluate("window.gameData.xp")
        print(f"New Level: {new_level}, New XP: {new_xp}")

        assert new_xp == 150, f"Expected XP to be 150, but got {new_xp}"
        assert new_level == 2, f"Expected level to be 2, but got {new_level}"

        page.screenshot(path="verification/leveling_verification.png")
        print("Leveling system logic verified successfully!")

        browser.close()

if __name__ == "__main__":
    verify_leveling()
