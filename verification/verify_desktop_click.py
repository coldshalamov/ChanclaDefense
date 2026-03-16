from playwright.sync_api import sync_playwright
import time
import os
import json

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # NOT mobile, to test desktop mouse events
        context = browser.new_context(viewport={'width': 800, 'height': 800})
        page = context.new_page()

        cwd = os.getcwd()
        page.goto(f"file://{cwd}/index.html")

        # Set fake game data with 1 unclaimed achievement
        game_data = {
            "coins": 0,
            "upgrades": {"lives": 0, "shield": 0, "cooldown": 0, "speed": 0},
            "bestScore": 0,
            "stats": {
                "totalSlaps": 105, # Completes "Novice Slapper" (target 100)
                "perfectSlaps": 0,
                "gamesPlayed": 0,
                "totalCoinsEarned": 0
            },
            "achievements": {}
        }

        game_data_json = json.dumps(game_data)
        page.evaluate(f"localStorage.setItem('chancla_bomb_save', JSON.stringify({game_data_json}))")
        page.reload()

        page.wait_for_selector("#game")

        # Give it a sec to load
        time.sleep(1)

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

        # Click first unclaimed achievement ("Novice Slapper")
        # Y position: 150 to 240
        page.evaluate("""
            const canvas = document.getElementById('game');
            const rect = canvas.getBoundingClientRect();
            const clickEvent = new MouseEvent('click', {
                clientX: rect.left + 225 * (rect.width / canvas.width),
                clientY: rect.top + 200 * (rect.height / canvas.height)
            });
            canvas.dispatchEvent(clickEvent);
        """)

        time.sleep(1)

        # Verify coins went up by 50 (Novice reward)
        coins = page.evaluate("JSON.parse(localStorage.getItem('chancla_bomb_save')).coins")
        print(f"Coins after desktop claim: {coins}")
        if coins == 50:
            print("Desktop achievement successfully claimed!")
        else:
            print("Failed to claim desktop achievement.")

        browser.close()

if __name__ == "__main__":
    run()
