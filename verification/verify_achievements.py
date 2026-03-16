import json
from playwright.sync_api import sync_playwright
import time
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 450, 'height': 800}, has_touch=True, is_mobile=True)
        page = context.new_page()

        cwd = os.getcwd()
        page.goto(f"file://{cwd}/index.html")

        # Set fake game data with 2 unclaimed achievements and 1 claimed
        game_data = {
            "coins": 0,
            "upgrades": {"lives": 0, "shield": 0, "cooldown": 0, "speed": 0},
            "bestScore": 0,
            "stats": {
                "totalSlaps": 105, # Completes "Novice Slapper" (target 100)
                "perfectSlaps": 260, # Completes "Good Eye" (50) and "Flawless" (250)
                "gamesPlayed": 2,
                "totalCoinsEarned": 0
            },
            "achievements": {
                "novice": True # Claimed
            }
        }

        # Proper JSON encoding for evaluate
        game_data_json = json.dumps(game_data)
        page.evaluate(f"localStorage.setItem('chancla_bomb_save', JSON.stringify({game_data_json}))")
        page.reload()

        page.wait_for_selector("#game")

        # Title Screen screenshot (should have red dot with "2")
        time.sleep(1)
        page.screenshot(path="verification/title_screen_achievements.png")

        # Click Achievements Button (110, 520, w, 46) -> center is around x=225, y=543
        page.evaluate("""
            const canvas = document.getElementById('game');
            const rect = canvas.getBoundingClientRect();
            const clickEvent = new MouseEvent('click', {
                clientX: rect.left + 225 * (rect.width / canvas.width),
                clientY: rect.top + 543 * (rect.height / canvas.height)
            });
            canvas.dispatchEvent(clickEvent);
        """)

        time.sleep(1)

        # Achievements Screen screenshot (should show 1 claimed, 2 completed but unclaimed, rest uncompleted)
        page.screenshot(path="verification/achievements_screen.png")

        # Click first unclaimed achievement ("Good Eye")
        # Y position calculation:
        # ach 0: "Novice" (claimed) -> 150 to 240
        # ach 1: "Pro" -> 255 to 345
        # ach 2: "Master" -> 360 to 450
        # ach 3: "Good Eye" (unclaimed) -> 465 to 555
        page.evaluate("""
            const canvas = document.getElementById('game');
            const rect = canvas.getBoundingClientRect();

            // Dispatch a touch event since it handles touch properly
            const e = new Event('touchstart');
            e.touches = [{
                clientX: rect.left + 225 * (rect.width / canvas.width),
                clientY: rect.top + 510 * (rect.height / canvas.height)
            }];
            canvas.dispatchEvent(e);

            const e2 = new Event('touchend');
            e2.changedTouches = [{
                clientX: rect.left + 225 * (rect.width / canvas.width),
                clientY: rect.top + 510 * (rect.height / canvas.height)
            }];
            canvas.dispatchEvent(e2);
        """)

        time.sleep(1)

        # Screenshot after claiming
        page.screenshot(path="verification/achievements_claimed.png")

        # Verify coins went up by 100 (Good Eye reward)
        coins = page.evaluate("JSON.parse(localStorage.getItem('chancla_bomb_save')).coins")
        print(f"Coins after claim: {coins}")
        if coins == 100:
            print("Achievement successfully claimed!")
        else:
            print("Failed to claim achievement.")

        browser.close()

if __name__ == "__main__":
    run()
