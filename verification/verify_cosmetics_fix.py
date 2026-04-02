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

    page.goto(f"file://{abs_path}")
    page.wait_for_timeout(1000)

    # 1. Screenshot Title Screen
    page.screenshot(path="verification/title_screen_with_hats_button_fixed.png")
    print("Screenshot taken: verification/title_screen_with_hats_button_fixed.png")

    # 2. Click Hats
    page.mouse.click(200, 613)
    page.wait_for_timeout(500)

    # 3. Screenshot Cosmetics menu
    page.screenshot(path="verification/cosmetics_menu_fixed.png")
    print("Screenshot taken: verification/cosmetics_menu_fixed.png")

    browser.close()

if __name__ == '__main__':
    with sync_playwright() as p:
        run(p)
