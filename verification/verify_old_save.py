import os
import sys
from playwright.sync_api import sync_playwright

def test_old_save():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        file_path = f"file://{os.path.abspath('index.html')}"

        # Load the game and manually set a save file WITHOUT the wins variable
        page.goto(file_path)
        page.evaluate("""() => {
            const save = { coins: 0, upgrades: { lives: 0, shield: 0, cooldown: 0, speed: 0 }, bestScore: 0, stats: { totalSlaps: 0, perfectSlaps: 0, gamesPlayed: 0, totalCoinsEarned: 0 }, achievements: {}, cosmetics: ['none'], currentHat: 'none' };
            localStorage.setItem('chancla_bomb_save', JSON.stringify(save));
        }""")

        # Reload to apply the new wins level
        page.goto(file_path)
        page.wait_for_timeout(1000)

        # Verify internal variables have been populated to wins = 1 correctly
        page.evaluate("""() => {
            const script = document.querySelector('script').textContent;
            const newScript = script.replace('})();', 'window.gameData = gameData; window.isa = isa; window.baseSpeed = baseSpeed; window.spawnInterval = spawnInterval; })();');
            const el = document.createElement('script');
            el.textContent = newScript;
            document.body.appendChild(el);
        }""")

        # Give it a moment to re-evaluate the IIFE
        page.wait_for_timeout(500)

        wins_level = page.evaluate("window.gameData.stats.wins")
        isa_anger = page.evaluate("window.isa.maxAnger")
        base_speed = page.evaluate("window.baseSpeed")
        spawn_interval = page.evaluate("window.spawnInterval")

        print(f"Verified legacy save migrated: Wins = {wins_level}, Max Anger = {isa_anger}, Base Speed = {base_speed}, Spawn Interval = {spawn_interval}")
        if wins_level != 1 or isa_anger != 100 or base_speed != 140 or spawn_interval != 1.2:
            print("ERROR: Legacy migration failed.")
            sys.exit(1)
        else:
            print("SUCCESS: Legacy migration succeeded.")

        browser.close()

if __name__ == "__main__":
    test_old_save()
