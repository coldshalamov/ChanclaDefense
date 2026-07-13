from playwright.sync_api import sync_playwright

def run_cuj(page):
    page.goto("file:///app/index.html")
    page.wait_for_timeout(500)

    # Inject to make golden chanclas spawn 100% of time for testing
    page.evaluate("""
        const oldRandom = Math.random;
        Math.random = () => {
            // Force Math.random() to return 0.01 which makes isGolden true
            // if we are checking < 0.05
            return 0.01;
        };
    """)

    # Click to start game
    page.click("canvas")
    page.wait_for_timeout(1000)

    # Take screenshot of it spawning
    page.screenshot(path="/home/jules/verification/screenshots/golden_spawn.png")
    page.wait_for_timeout(200)

    # Slap it
    page.click("canvas")
    page.wait_for_timeout(200)

    # Take screenshot of the slap effect
    page.screenshot(path="/home/jules/verification/screenshots/golden_slap.png")
    page.wait_for_timeout(1000)

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="/home/jules/verification/videos"
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()  # MUST close context to save the video
            browser.close()
