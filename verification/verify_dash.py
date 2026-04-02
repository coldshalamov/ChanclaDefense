from playwright.sync_api import sync_playwright
import os

def test_dash_feature(page):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    file_path = f"file://{parent_dir}/index.html"

    page.goto(file_path)

    # Wait for the game canvas to load
    page.wait_for_selector('canvas#game')

    # Start game by clicking play button area or pressing enter
    box = page.locator('canvas#game').bounding_box()
    # click in the play button area on the title screen
    page.mouse.click(box['x'] + box['width']/2, box['y'] + 400)
    page.wait_for_timeout(500)

    # Trigger Dash
    page.keyboard.down('Shift')
    page.wait_for_timeout(50)
    page.keyboard.up('Shift')

    page.wait_for_timeout(50) # Wait mid dash

    # Take screenshot of the dash effect on the canvas
    page.locator('canvas#game').screenshot(path="/home/jules/verification/dash_verification.png")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        try:
            test_dash_feature(page)
        finally:
            browser.close()
