from playwright.sync_api import sync_playwright

with open("index.html", "r") as f:
    content = f.read()

# Force golden spawn and force game state immediately
content = content.replace("let state = STATE.TITLE;", "let state = STATE.PLAYING;")
content = content.replace("const isGolden = Math.random() < 0.05;", "const isGolden = true;")

with open("index_test_gold.html", "w") as f:
    f.write(content)

def run_cuj(page):
    page.goto("file:///app/index_test_gold.html")
    page.wait_for_timeout(500)

    # Wait for chancla to drop
    page.wait_for_timeout(1000)

    # Take screenshot of it spawning
    page.screenshot(path="/home/jules/verification/screenshots/golden_spawn.png")
    page.wait_for_timeout(200)

    # Slap it perfectly (center of screen)
    page.mouse.click(200, 600)
    page.wait_for_timeout(100)

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
