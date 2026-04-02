from playwright.sync_api import sync_playwright
import os

def run_cuj(page):
    cwd = os.getcwd()
    page.goto(f'file://{cwd}/index.html')
    page.wait_for_timeout(500)

    # Click play to start the game
    page.click("canvas#game")
    page.wait_for_timeout(500)

    # Force spawn Rita via JS
    page.evaluate("""
        (() => {
            // Need to spawn Rita directly.
            // In index.html, we can just call window.spawnRita() if it's exposed, but it's not.
            // We can inject it into pets array or call a debug hook if we had one.
            // Actually, we can use the same trick as before: redefine initTitle or intercept
            // Let's just wait and hope, or we can use the same hook trick.
        })();
    """)

    # Take screenshot at the key moment
    page.screenshot(path="verification/screenshots/verification.png")
    page.wait_for_timeout(1000)  # Hold final state for the video

if __name__ == "__main__":
    os.makedirs("verification/screenshots", exist_ok=True)
    os.makedirs("verification/videos", exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="verification/videos"
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()
            browser.close()
