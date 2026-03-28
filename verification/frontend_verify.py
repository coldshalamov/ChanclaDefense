import os
import time
from playwright.sync_api import sync_playwright

def frontend_verify():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 450, 'height': 800}, has_touch=True, is_mobile=True)
        page = context.new_page()

        file_path = f"file://{os.path.abspath('index.html')}"

        # Initialize mock save without xp and level
        page.add_init_script("""
            const mockSave = {
                xp: 2500,
                level: 8,
                coins: 0,
                upgrades: { lives: 0, shield: 0, cooldown: 0, speed: 0 },
                bestScore: 0,
                stats: { totalSlaps: 0, perfectSlaps: 0, gamesPlayed: 0, totalCoinsEarned: 0 }
            };
            localStorage.setItem('chancla_bomb_save', JSON.stringify(mockSave));
        """)

        page.goto(file_path)

        # Wait for the game to initialize Title Screen
        time.sleep(1)

        # Take screenshot of the Title Screen (which should have Level displayed)
        page.screenshot(path="verification/frontend_title.png")

        # Start game by simulating click on Play button
        page.mouse.click(200, 400)
        time.sleep(1)

        # Take screenshot of the HUD (which should have Level displayed)
        page.screenshot(path="verification/frontend_playing.png")
        print("Frontend screenshots saved.")

        browser.close()

if __name__ == "__main__":
    frontend_verify()
