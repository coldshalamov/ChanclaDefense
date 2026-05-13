import os
import sys
from playwright.sync_api import sync_playwright

def test_wins_scaling():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        file_path = f"file://{os.path.abspath('index.html')}"

        # Load the game and manually set stats.wins to 5 in localStorage
        page.goto(file_path)
        page.evaluate("""() => {
            const save = JSON.parse(localStorage.getItem('chancla_bomb_save') || '{}');
            save.stats = save.stats || {};
            save.stats.wins = 5;
            localStorage.setItem('chancla_bomb_save', JSON.stringify(save));
        }""")

        # Reload to apply the new wins level
        page.goto(file_path)
        page.wait_for_timeout(1000)

        page.screenshot(path="verification/wins_title.png")
        print("Level 5 Title screen screenshot taken.")

        # Start game and verify stats via injected code
        page.evaluate("""() => {
            const script = document.querySelector('script').textContent;
            const newScript = script.replace('})();', 'window.isa = isa; window.baseSpeed = baseSpeed; window.spawnInterval = spawnInterval; window.gameData = gameData; window.triggerWin = triggerWin; window.state = state; window.STATE = STATE; })();');
            const el = document.createElement('script');
            el.textContent = newScript;
            document.body.appendChild(el);
        }""")

        # Give it a moment to re-evaluate the IIFE
        page.wait_for_timeout(500)

        # Simulate pressing Enter to start playing
        page.keyboard.press("Enter")
        page.wait_for_timeout(100)

        # Verify internal variables
        isa_anger = page.evaluate("window.isa.maxAnger")
        base_speed = page.evaluate("window.baseSpeed")
        spawn_interval = page.evaluate("window.spawnInterval")
        wins_level = page.evaluate("window.gameData.stats.wins")

        print(f"Verified internally: Max Anger = {isa_anger}, Base Speed = {base_speed}, Spawn Interval = {spawn_interval}, Wins Level = {wins_level}")

        # Trigger Win manually
        page.evaluate("window.triggerWin()")
        page.wait_for_timeout(1000)

        page.screenshot(path="verification/wins_win_screen.png")
        print("Level 5 Win screen screenshot taken.")

        new_wins_level = page.evaluate("window.gameData.stats.wins")
        print(f"New Wins Level after win: {new_wins_level}")

        browser.close()

if __name__ == "__main__":
    test_wins_scaling()
