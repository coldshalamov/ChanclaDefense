from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the game from the file
        filepath = os.path.abspath("chancla_bomb.html")
        page.goto(f"file://{filepath}")

        # Wait for canvas
        page.wait_for_selector("#game")

        # Take initial title screenshot
        page.screenshot(path="verification/title_screen.png")
        print("Title screen captured.")

        canvas = page.locator("#game")
        box = canvas.bounding_box()

        # Click Shop button (force=True to bypass overlays)
        canvas.click(position={"x": box["width"] * 0.5, "y": box["height"] * (463/700)}, force=True)

        # Wait a bit for render
        page.wait_for_timeout(500)

        # Take shop screenshot
        page.screenshot(path="verification/shop_screen.png")
        print("Shop screen captured.")

        # Click Back button
        canvas.click(position={"x": box["width"] * 0.5, "y": box["height"] * (645/700)}, force=True)

        page.wait_for_timeout(500)
        page.screenshot(path="verification/back_to_title.png")
        print("Back to title captured.")

        browser.close()

if __name__ == "__main__":
    run()
