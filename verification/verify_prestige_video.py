from playwright.sync_api import sync_playwright
import os
import glob
import time

def run_cuj(page):
    # Set the game state to have >= 10 wins (level 10+)
    # By injecting a small script, or by evaluating javascript after load
    page.goto('file://' + os.path.abspath('index.html'))
    page.wait_for_timeout(1000)

    # We need to set local storage to have 10 wins to show prestige
    page.evaluate('''
        const data = {
            coins: 500,
            upgrades: { lives: 3, shield: 1, cooldown: 5, speed: 5, power: 5 },
            bestScore: 100,
            stats: { totalSlaps: 50, perfectSlaps: 10, gamesPlayed: 5, totalCoinsEarned: 500, wins: 10 },
            achievements: {},
            cosmetics: ['none'],
            currentHat: 'none',
            prestige: 0
        };
        localStorage.setItem('chancla_bomb_save', JSON.stringify(data));
    ''')
    page.reload()
    page.wait_for_timeout(1000)

    # Click on Title Screen to Prestige
    # Button is around x=canvas.width/2, y=643 (620 to 666)
    # The canvas scales, so let's get the bounding rect
    box = page.locator('canvas#game').bounding_box()
    if box:
        # Scale coords for original 600x800 canvas
        scaleX = box['width'] / 600
        scaleY = box['height'] / 800

        click_x = box['x'] + 300 * scaleX
        click_y = box['y'] + 643 * scaleY

        page.mouse.click(click_x, click_y)
        page.wait_for_timeout(1000)

        # Take a screenshot of the prestige menu
        page.screenshot(path="/home/jules/verification/screenshots/prestige_menu.png")
        page.wait_for_timeout(500)

        # Click the "Prestige Now!" button
        # (x=300, y=800-125 = 675)
        prestige_btn_y = box['y'] + 675 * scaleY
        page.mouse.click(click_x, prestige_btn_y)
        page.wait_for_timeout(1000)

        page.screenshot(path="/home/jules/verification/screenshots/prestige_done.png")
        page.wait_for_timeout(1000)

if __name__ == "__main__":
    os.makedirs("/home/jules/verification/videos", exist_ok=True)
    os.makedirs("/home/jules/verification/screenshots", exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="/home/jules/verification/videos"
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()  # MUST close context to save the video
            browser.close()
