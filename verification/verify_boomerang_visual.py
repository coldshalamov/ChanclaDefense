from playwright.sync_api import sync_playwright

def run_cuj(page):
    page.goto("file:///app/temp_index.html")
    page.wait_for_timeout(500)

    # Insert a boomerang chancla moving very fast down so we can catch it swooping up
    page.evaluate("""
        window.gameApp.player.x = 20; // move player out of the way
        window.gameApp.chanclas.push({
            x: 200, y: 550, vx: 0, vy: 600, w: 34, h: 34,
            type: 'boomerang', rotation: 0, rotSpeed: 5, returning: false, slapped: false
        });
    """)
    page.wait_for_timeout(200) # Should hit bottom and bounce
    page.screenshot(path="/app/verification/screenshots/boomerang_swoop.png")
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
