from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the local HTML file
        url = f"file://{os.getcwd()}/chancla_bomb.html"
        print(f"Navigating to {url}")
        page.goto(url)

        # Wait for canvas to be present
        page.wait_for_selector("#game")

        # Wait a bit for init
        page.wait_for_timeout(1000)

        # Take screenshot of Title Screen
        page.screenshot(path="verification/title_screen.png")
        print("Title screen screenshot taken.")

        game_canvas = page.locator("#game")
        box = game_canvas.bounding_box()

        if not box:
            print("Could not find bounding box for #game")
            return

        # Shop button Center: 440. Height 700.
        # X center: 0.5
        click_x = box['x'] + box['width'] * 0.5
        click_y = box['y'] + box['height'] * (440/700)

        print(f"Canvas box: {box}")
        print(f"Clicking at {click_x}, {click_y}")

        # Perform click
        page.mouse.click(click_x, click_y)

        # Wait a bit for transition
        page.wait_for_timeout(1000)

        # Take screenshot of Shop
        page.screenshot(path="verification/shop_screen.png")
        print("Shop screen screenshot taken.")

        browser.close()

if __name__ == "__main__":
    run()
