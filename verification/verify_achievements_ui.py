import os
from playwright.sync_api import sync_playwright

def verify_achievements():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Configure viewport to mobile size as required by memory
        context = browser.new_context(
            viewport={'width': 450, 'height': 800},
            has_touch=True,
            is_mobile=True
        )
        page = context.new_page()

        # Load the game locally
        file_url = 'file://' + os.path.abspath('index.html')

        # We need to expose the game state to test the achievements screen.
        # Since it's inside an IIFE, we modify the DOM slightly before playing.
        html_path = 'index.html'
        with open(html_path, 'r') as f:
            content = f.read()

        # Replace the end of the IIFE to expose `state`
        modified_content = content.replace(
            "initTitle();\n        })();",
            "initTitle();\n        window.setState = (s) => { state = s; };\n        })();"
        )

        # Write temporary file
        temp_path = 'temp_index.html'
        with open(temp_path, 'w') as f:
            f.write(modified_content)

        file_url = 'file://' + os.path.abspath(temp_path)

        page.goto(file_url)
        page.wait_for_timeout(500)

        save_data = '{"coins": 100, "upgrades": {"lives": 0, "shield": 0, "cooldown": 0, "speed": 0}, "bestScore": 50, "stats": {"totalSlaps": 105, "perfectSlaps": 5, "gamesPlayed": 5, "totalCoinsEarned": 100}, "achievements": {"first_blood": true}}'
        page.evaluate(f"window.localStorage.setItem('chancla_bomb_save', '{save_data}');")
        page.reload()
        page.wait_for_timeout(500)

        # Force state to achievements
        page.evaluate("window.setState('achievements');")
        page.wait_for_timeout(500)

        # Take screenshot of the achievements screen
        os.makedirs('verification', exist_ok=True)
        screenshot_path = 'verification/achievements_menu.png'
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

        browser.close()
        os.remove(temp_path)

if __name__ == "__main__":
    verify_achievements()