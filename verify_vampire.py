from playwright.sync_api import sync_playwright

def run_cuj(page):
    page.goto("file:///app/index.html")
    page.wait_for_timeout(500)

    # Click the canvas to start the game
    page.mouse.click(200, 400)
    page.wait_for_timeout(500)

    # Inject a vampire chancla by patching the global window context or using eval
    page.evaluate('''
        // Hack: temporarily expose chanclas array
        if (typeof window.chanclas === "undefined") {
            window.chanclas = [];
        }
        chanclas.push({
            x: 200, y: 150, vx: 0, vy: 50, w: 34, h: 24, type: "vampire", rotation: 0, rotSpeed: 0, vampirePhase: 0
        });
    ''')
    page.wait_for_timeout(500)

    # Wait for the chancla to come down
    page.wait_for_timeout(1000)

    # Slap the vampire chancla
    # We will just press space which tries to slap all near ones (might not be in range, so we move player)
    # The game uses mouse movement or arrow keys for player movement
    # Move the player towards center just in case
    page.mouse.move(200, 600)
    page.keyboard.press("Space")
    page.wait_for_timeout(200)

    # Take screenshot at the key moment showing the vampire
    page.screenshot(path="/app/verification.png")
    page.wait_for_timeout(1000)  # Hold final state for the video

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="/app/videos",
            viewport={"width": 420, "height": 740}
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()  # MUST close context to save the video
            browser.close()
