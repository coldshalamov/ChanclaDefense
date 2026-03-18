import os
import time
from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    # Configure context to simulate mobile touch environment
    context = browser.new_context(
        viewport={'width': 450, 'height': 800},
        has_touch=True,
        is_mobile=True,
        record_video_dir="verification/video"
    )

    # Load game data with some achievements completed but not claimed
    # high_roller completed (bestScore >= 150)
    # first_blood completed (totalSlaps >= 1)
    init_script = """
        const testData = {
            coins: 50,
            upgrades: { lives: 0, shield: 0, cooldown: 0, speed: 0 },
            bestScore: 160,
            stats: { totalSlaps: 5, perfectSlaps: 0, gamesPlayed: 2, totalCoinsEarned: 50 },
            achievements: {}
        };
        localStorage.setItem('chancla_bomb_save', JSON.stringify(testData));
    """

    page = context.new_page()
    page.add_init_script(init_script)

    file_url = f"file://{os.path.abspath('index.html')}"
    page.goto(file_url)

    # Wait for the title screen to render
    page.wait_for_timeout(1000)
    page.screenshot(path="verification/title_screen_achievements.png")

    # Click the Achievements button on title screen
    # Its coordinates are roughly x=110 to width-110, y=480 to 520
    # Center is approximately x=225, y=500
    page.mouse.click(225, 500)
    page.wait_for_timeout(1000)

    # Screenshot of the Achievements page
    page.screenshot(path="verification/achievements_page.png")

    # Click the "CLAIM" button for "First Slap" (y=120 + 42 = 162)
    page.mouse.click(350, 160)
    page.wait_for_timeout(500)

    # Click the "CLAIM" button for "High Roller" (y=120 + 85*4 + 42 = 502)
    page.mouse.click(350, 480)
    page.wait_for_timeout(1000)

    # Screenshot after claiming
    page.screenshot(path="verification/achievements_claimed.png")

    # Click the Back button (y = canvas.height - 65 + 22 = 800 - 65 + 22 = 757, but game scales so maybe around 650)
    page.mouse.click(225, 660)
    page.wait_for_timeout(1000)

    # Screenshot back at title screen
    page.screenshot(path="verification/title_screen_returned.png")

    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
