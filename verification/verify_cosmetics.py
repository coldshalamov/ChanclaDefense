from playwright.sync_api import sync_playwright
import os

def run(playwright):
    browser = playwright.chromium.launch(headless=True)

    context = browser.new_context(
        viewport={'width': 400, 'height': 700},
        has_touch=True,
        is_mobile=True,
        device_scale_factor=1
    )

    page = context.new_page()

    abs_path = os.path.abspath('index.html')

    with open('index.html', 'r') as f:
        html_content = f.read()

    html_content = html_content.replace(
        '})();',
        'window.state = state; window.gameData = gameData; window.COSMETICS_LIST = COSMETICS_LIST; })();'
    )
    html_content = html_content.replace(
        'if (gameData.coins === undefined) gameData.coins = 0;',
        'if (gameData.coins === undefined) gameData.coins = 1500;'
    )

    page.route(f"file://{abs_path}", lambda route: route.fulfill(body=html_content, content_type="text/html"))
    page.goto(f"file://{abs_path}")

    page.wait_for_timeout(1000)

    # 1. Screenshot Title Screen
    page.screenshot(path="verification/title_screen_with_hats_button.png")
    print("Screenshot taken: verification/title_screen_with_hats_button.png")

    # 2. Open Cosmetics Menu
    print("Opening Cosmetics Menu...")
    # Cosmetics Button bounds: pos.y >= 590 && pos.y <= 636 && pos.x >= 110 && pos.x <= canvas.width - 110
    page.mouse.click(200, 613)
    page.wait_for_timeout(500)

    # 3. Screenshot Cosmetics Menu empty state
    page.screenshot(path="verification/cosmetics_menu.png")
    print("Screenshot taken: verification/cosmetics_menu.png")

    # 4. Buy 'sunglasses' (cost 400)
    print("Buying sunglasses...")
    # 'none' 220, 'cap' 290, 'party' 360, 'sunglasses' 430
    page.mouse.click(200, 460) # y=430 to 490
    page.wait_for_timeout(500)
    page.screenshot(path="verification/cosmetics_menu_sunglasses_bought.png")

    # 5. Go back to title
    print("Returning to Title...")
    page.mouse.click(200, 670)
    page.wait_for_timeout(500)

    # 6. Start Game and verify player has sunglasses
    print("Starting Game to verify player hat...")
    # Play Button pos.y >= 380 && pos.y <= 426
    page.mouse.click(200, 400)
    page.wait_for_timeout(1000)

    # 7. Screenshot Player with Sunglasses in game
    page.screenshot(path="verification/player_with_sunglasses.png")
    print("Screenshot taken: verification/player_with_sunglasses.png")

    browser.close()

if __name__ == '__main__':
    with sync_playwright() as p:
        run(p)
