
from playwright.sync_api import sync_playwright
import time
import os
import json

def verify_persistence():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        cwd = os.getcwd()
        url = 'file://' + cwd + '/chancla_bomb.html'

        print(f"Loading {url}")
        page.goto(url)

        # 1. Start Game
        canvas = page.locator('#game')
        # Click Play button (approx 200, 400)
        canvas.click(position={'x': 200, 'y': 400})
        time.sleep(1)

        # 2. Inject state to near achievement
        # 'slap_100' target 100. Set slaps to 99.
        print("Injecting stats...")
        page.evaluate("""
            window.gameInternals.gameData.stats.slaps = 99;
        """)

        # 3. Perform action (Slap)
        # We need a chancla to slap. Spawning one close to player.
        page.evaluate("""
            const p = window.gameInternals.player;
            window.gameInternals.chanclas.push({
                x: p.x, y: p.y,
                vx: 0, vy: 0,
                w: 30, h: 30,
                type: 'normal',
                rotation: 0, rotSpeed: 0
            });
        """)

        # Trigger slap
        page.keyboard.press('Space')
        time.sleep(0.5)

        # 4. Verify Stats Increment
        slaps = page.evaluate("window.gameInternals.gameData.stats.slaps")
        print(f"Slaps after action: {slaps}")
        assert slaps == 100, f"Expected 100 slaps, got {slaps}"

        # 5. Verify Achievement Unlocked
        achievements = page.evaluate("window.gameInternals.gameData.achievements")
        print(f"Achievements: {achievements}")
        assert 'slap_100' in achievements, "Achievement 'slap_100' not found in achievements"

        # 6. Verify Persistence after Reload
        print("Reloading page...")
        page.reload()

        time.sleep(1)

        persisted_slaps = page.evaluate("window.gameInternals.gameData.stats.slaps")
        persisted_achievements = page.evaluate("window.gameInternals.gameData.achievements")

        print(f"Persisted Slaps: {persisted_slaps}")
        print(f"Persisted Achievements: {persisted_achievements}")

        assert persisted_slaps == 100, f"Persisted slaps expected 100, got {persisted_slaps}"
        assert 'slap_100' in persisted_achievements, "Persisted achievement 'slap_100' missing"

        browser.close()
        print("Persistence Verification Passed!")

if __name__ == '__main__':
    verify_persistence()
