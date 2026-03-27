from playwright.sync_api import sync_playwright
import os

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={'width': 450, 'height': 800},
        has_touch=True,
        is_mobile=True
    )
    page = context.new_page()

    # Load game
    abs_path = os.path.abspath('index.html')

    # Inject localStorage save with coins and an owned but not equipped hat
    init_script = """
    const saveData = {
        coins: 1000,
        upgrades: { lives: 0, shield: 0, cooldown: 0, speed: 0 },
        bestScore: 0,
        stats: { totalSlaps: 0, perfectSlaps: 0, gamesPlayed: 0, totalCoinsEarned: 1000 },
        achievements: {},
        cosmetics: ['cap'],
        currentHat: null
    };
    localStorage.setItem('chancla_bomb_save', JSON.stringify(saveData));
    """
    page.add_init_script(init_script)

    page.goto(f'file://{abs_path}')
    page.wait_for_timeout(500)

    # Title Screen Screenshot
    page.screenshot(path="verification/title_with_cosmetics_btn.png")

    # Navigate to Cosmetics Screen
    # Cosmetics Button (110, 590, w, 46) on 400x700 scaled canvas
    canvas = page.locator('canvas#game')
    box = canvas.bounding_box()

    scale_x = box['width'] / 400
    scale_y = box['height'] / 700

    # Click Cosmetics button
    click_x = box['x'] + (400 / 2) * scale_x
    click_y = box['y'] + 610 * scale_y
    page.mouse.click(click_x, click_y)
    page.wait_for_timeout(500)

    page.screenshot(path="verification/cosmetics_screen_initial.png")

    # Click 'cap' to equip it (y=110, h=60)
    click_cap_y = box['y'] + 140 * scale_y
    page.mouse.click(click_x, click_cap_y)
    page.wait_for_timeout(200)

    # Click 'cowboy' to purchase it (y=110+70=180)
    click_cowboy_y = box['y'] + 210 * scale_y
    page.mouse.click(click_x, click_cowboy_y)
    page.wait_for_timeout(200)

    page.screenshot(path="verification/cosmetics_screen_purchased.png")

    # Click Back Button (100, canvas.height - 70, w, 46) -> 700 - 70 = 630
    click_back_y = box['y'] + 650 * scale_y
    page.mouse.click(click_x, click_back_y)
    page.wait_for_timeout(500)

    # Start game to see hat
    # Play Button (110, 380, w, 46)
    click_play_y = box['y'] + 400 * scale_y
    page.mouse.click(click_x, click_play_y)
    page.wait_for_timeout(500)

    page.screenshot(path="verification/gameplay_with_hat.png")

    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
