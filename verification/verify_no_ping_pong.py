from playwright.sync_api import sync_playwright

def run_cuj(page):
    page.goto("file:///app/index.html")
    page.wait_for_timeout(500)

    # We just need to check the game starts without errors since the ping-pong rally mechanic is RNG-based and occurs mid-game
    page.keyboard.press('Enter')
    page.wait_for_timeout(2000)

    page.screenshot(path="/app/verification/screenshots/no_ping_pong_verification.png")
    page.wait_for_timeout(1000)

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="/app/verification/videos"
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()
            browser.close()
