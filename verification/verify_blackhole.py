from playwright.sync_api import sync_playwright
import os
import time

def run():
    print("Running verification script...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        os.makedirs("/app/verification/videos", exist_ok=True)
        context = browser.new_context(record_video_dir="/app/verification/videos/")
        page = context.new_page()

        page.goto("file:///app/temp_test.html")

        # Start game
        page.keyboard.press("Enter")
        time.sleep(0.5)

        # Inject a black hole chancla
        page.evaluate("""
            window.internalState.chanclas.push({
                x: 200, y: 150, vx: 0, vy: 50, w: 36, h: 36, type: 'blackhole', rotation: 0, rotSpeed: 5
            });
        """)
        time.sleep(0.5)

        # Take a screenshot before slap
        page.screenshot(path="/app/verification/before_slap.png")

        # Slap it
        page.evaluate("window.internalState.player.x = 200; window.internalState.player.y = 200;")
        page.keyboard.press("Space")
        time.sleep(1.0)

        # Take screenshot during black hole active
        page.screenshot(path="/app/verification/active_blackhole.png")

        context.close()
        browser.close()
    print("Done")

if __name__ == "__main__":
    run()
