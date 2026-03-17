import os
import time
from playwright.sync_api import sync_playwright

def verify_achievements():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Mobile viewport since game is mobile-first
        context = browser.new_context(viewport={'width': 450, 'height': 800}, is_mobile=True, has_touch=True)
        page = context.new_page()

        # We need to setup some fake stats to show progress
        page.add_init_script("""
            localStorage.setItem('chancla_bomb_save', JSON.stringify({
                coins: 100,
                upgrades: { lives: 0, shield: 0, cooldown: 0, speed: 0 },
                bestScore: 25,
                stats: { totalSlaps: 150, perfectSlaps: 20, gamesPlayed: 10, totalCoinsEarned: 100 },
                achievements: { 'slaps_100': true } // One claimed, others partial/ready
            }));
        """)

        file_url = 'file://' + os.path.abspath('index.html')
        page.goto(file_url)

        time.sleep(1) # Let it render

        # Click the new achievements button on Title screen (y=520 to 566)
        # Center x is 225. Button is at y=520, h=46 => center y=543
        page.mouse.click(225, 543)
        time.sleep(1) # Wait for render

        # Take screenshot of the achievements screen
        os.makedirs('verification', exist_ok=True)
        screenshot_path = 'verification/achievements_screen.png'
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

        browser.close()

if __name__ == "__main__":
    verify_achievements()
