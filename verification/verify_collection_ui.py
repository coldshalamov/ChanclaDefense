
from playwright.sync_api import sync_playwright
import time
import os

def verify_collection_ui():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Use a viewport that results in predictable scaling if possible,
        # but here we calculated that with default viewport, scale is ~0.952.
        # Canvas W=400, CSS W=420.
        page = browser.new_page(viewport={'width': 1280, 'height': 800})

        cwd = os.getcwd()
        url = 'file://' + cwd + '/chancla_bomb.html'

        print(f"Loading {url}")
        page.goto(url)

        # 1. Click Collection Button
        # Button is approx at y=520-566 (Canvas Units). Center ~543.
        # Scale factor (approx) = 420/400 = 1.05 (CSS pixels per Canvas pixel)
        # So we need to click at 543 * 1.05 = ~570.
        canvas = page.locator('#game')
        print("Clicking Collection button...")
        # We use a slightly larger Y to account for scaling
        canvas.click(position={'x': 210, 'y': 570})

        time.sleep(0.5)
        page.screenshot(path='verification/collection_empty.png')
        print("Screenshot collection_empty.png taken")

        # 2. Inject achievements
        print("Injecting achievements...")
        page.evaluate("""
            window.gameInternals.gameData.achievements = ['first_slap', 'slap_100', 'perfect_10'];
            // Force redraw/update if needed, though loop handles it
        """)

        time.sleep(0.5)
        page.screenshot(path='verification/collection_filled.png')
        print("Screenshot collection_filled.png taken")

        browser.close()

if __name__ == '__main__':
    verify_collection_ui()
