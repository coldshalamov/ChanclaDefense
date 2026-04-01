import os
import glob
from playwright.sync_api import sync_playwright

def run_cuj(page):
    file_url = 'file://' + os.path.abspath('index.html')

    # We inject some coins to test purchasing logic easily
    page.goto(file_url)
    page.wait_for_timeout(500)

    # Inject coins into gameData to afford hats
    page.evaluate('''() => {
        let save = JSON.parse(localStorage.getItem('chancla_bomb_save') || '{}');
        save.coins = 1000;
        localStorage.setItem('chancla_bomb_save', JSON.stringify(save));
    }''')
    page.reload()
    page.wait_for_timeout(500)

    # Click cosmetics button on title screen
    # Hitbox is x: 110 to width-110, y: 590 to 636
    # Let's target center of the button
    box = page.locator('canvas').bounding_box()
    if not box: return

    btn_x = box['x'] + box['width'] / 2
    btn_y = box['y'] + 613

    page.mouse.click(btn_x, btn_y)
    page.wait_for_timeout(1000)

    # Take screenshot of cosmetics menu
    page.screenshot(path="/home/jules/verification/screenshots/cosmetics_menu.png")

    # Buy and equip the "Cowboy" hat (first item, y: 130 to 195)
    item1_y = box['y'] + 162
    page.mouse.click(btn_x, item1_y) # Click to buy
    page.wait_for_timeout(500)

    # Buy and equip the "Crown" hat (third item, y: 280 to 345)
    item3_y = box['y'] + 312
    page.mouse.click(btn_x, item3_y) # Click to buy
    page.wait_for_timeout(500)

    page.screenshot(path="/home/jules/verification/screenshots/cosmetics_menu_purchased.png")

    # Click Back button (y: height - 70 to height - 24)
    back_y = box['y'] + box['height'] - 47
    page.mouse.click(btn_x, back_y)
    page.wait_for_timeout(1000)

    # Click Play button (y: 380 to 426)
    play_y = box['y'] + 403
    page.mouse.click(btn_x, play_y)
    page.wait_for_timeout(1000)

    # Take screenshot of playing game with crown hat equipped
    page.screenshot(path="/home/jules/verification/screenshots/cosmetics_equipped.png")
    page.wait_for_timeout(1000)

if __name__ == "__main__":
    os.makedirs("/home/jules/verification/videos", exist_ok=True)
    os.makedirs("/home/jules/verification/screenshots", exist_ok=True)

    # Clear old videos
    for f in glob.glob("/home/jules/verification/videos/*.webm"):
        os.remove(f)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Mobile viewport configuration since game is mostly 420x700 max
        context = browser.new_context(
            record_video_dir="/home/jules/verification/videos",
            viewport={'width': 450, 'height': 800},
            is_mobile=True,
            has_touch=True
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()
            browser.close()
            print("Video recorded.")
