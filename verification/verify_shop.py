import os
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        # file path
        url = "file://" + os.path.abspath("index.html")
        page.goto(url)

        # Wait for canvas
        page.wait_for_selector("canvas")

        # Take title screenshot
        page.screenshot(path="verification/shop_title_before.png")
        print("Title screenshot taken")

        # Click Tiendita button (approx 200, 480)
        # Note: Canvas is 400x700.
        page.click("canvas", position={"x": 200, "y": 480})

        # Wait a bit for redraw
        page.wait_for_timeout(500)

        # Take shop screenshot
        page.screenshot(path="verification/shop_screen.png")
        print("Shop screenshot taken")

        # Click Back button (approx 200, 640)
        page.click("canvas", position={"x": 200, "y": 640})

        page.wait_for_timeout(500)
        page.screenshot(path="verification/shop_title_after.png")
        print("Back to title screenshot taken")

        browser.close()

if __name__ == "__main__":
    run()
