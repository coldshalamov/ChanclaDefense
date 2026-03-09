from playwright.sync_api import sync_playwright
import time
import os
import json

def verify_achievements():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the game from the file directly using absolute path
        cwd = os.getcwd()
        page.goto('file://' + cwd + '/index.html')

        print("Loaded index.html")

        # Wait for canvas
        canvas = page.locator('#game')
        box = canvas.bounding_box()

        if not box:
            print("Canvas not found!")
            return

        # Click Achievements Button
        # Button is x:110-290, y:520-566 (Internal 400x700)
        # Center approx 200, 543.
        click_y = box['height'] * (543 / 700)
        click_x = box['width'] * 0.5

        canvas.click(position={'x': click_x, 'y': click_y})
        print("Clicked Achievements Button")
        time.sleep(0.5)

        # Take screenshot of achievements screen
        page.screenshot(path='verification/achievements_screen.png')
        print("Achievements screen screenshot taken")

        # Go back to title (Back button at bottom)
        # y = 700 - 55 = 645. 645/700 = 0.92
        back_y = box['height'] * (645 / 700)
        canvas.click(position={'x': click_x, 'y': back_y})
        print("Clicked Back Button")
        time.sleep(0.5)

        # Start Game (Play button at 400ish)
        # y = 403. 403/700 = 0.57
        play_y = box['height'] * (403 / 700)
        canvas.click(position={'x': click_x, 'y': play_y})
        print("Clicked Play Button")
        time.sleep(1)

        # Trigger a slap (Spacebar) to get 1 slap
        # Note: Need chancla to be in range for it to count as a "hit" usually?
        # My code increments `stats.slaps` in `trySlap` ONLY IF `slappedAny` is true?
        # Let's check `trySlap` logic I wrote.
        # "gameData.stats.slaps++;" is inside "if (dist < slapRange) { ... }" block.
        # So I need to actually hit a chancla.
        # In 1 second, a chancla might have spawned.
        # `spawnInterval` is 1.2s initially. `timeElapsed` > 12 changes it.
        # So at t=1.0s, maybe no chancla yet?
        # `spawnTimer` starts at 0. `spawnInterval` 1.2.
        # Update loop: `spawnTimer += dt`. `if (spawnTimer >= spawnInterval)`.
        # So first chancla spawns at 1.2s.

        # I should wait longer.
        print("Waiting for spawn...")
        time.sleep(1.5)

        # Now chancla should be on screen.
        # Isa y=70. Chancla spawns at Isa.y + 40 = 110.
        # Falls down.
        # Player y = 700 - 70 = 630.
        # Base speed 140.
        # Distance ~500px. Time to reach player ~3.5s.

        # I need to wait until chancla is close to player.
        # Or I can just spam spacebar.

        print("Spamming spacebar...")
        for i in range(10):
            page.keyboard.press('Space')
            time.sleep(0.4) # Cooldown is ~0.3

        # Check localStorage
        save_data = page.evaluate("localStorage.getItem('chancla_bomb_save')")

        if save_data:
            data = json.loads(save_data)
            print("Game Data:", data)
            stats = data.get('stats', {})
            slaps = stats.get('slaps', 0)
            print(f"Slaps recorded: {slaps}")

            achievements = data.get('achievements', {})
            if achievements.get('first_slap'):
                print("SUCCESS: 'First Slap' achievement unlocked.")
            else:
                print("INFO: 'First Slap' not unlocked (maybe missed chanclas).")

            # If we missed all (which is possible with random movement), try "miss" logic?
            # But slaps stats only increment on hit in my code.

        else:
            print("FAILURE: No save data found.")

        browser.close()

if __name__ == '__main__':
    verify_achievements()
