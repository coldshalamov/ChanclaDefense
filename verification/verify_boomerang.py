from playwright.sync_api import sync_playwright

def run_cuj(page):
    page.goto("file:///app/index.html")
    page.wait_for_timeout(500)

    # Force Boomerang Chancla
    page.evaluate("""
        window.gameApp = (() => {
            let state = 'playing';
            let chanclas = [];
            let floatTexts = [];
            let score = 0;
            let player = { x: 200, y: 630, w: 55, h: 45, speed: 230, lives: 3, maxLives: 5, shield: false, hitTimer: 0 };
            const canvas = document.getElementById('game');

            // Expose vars for test
            window.testVars = { state, chanclas, floatTexts, score, player, canvas };
        })();

        // Setup initial playing state with a boomerang chancla falling
        state = 'playing';
        chanclas.push({
            x: 200, y: 350, vx: 0, vy: 200, w: 34, h: 34,
            type: 'boomerang', rotation: 0, rotSpeed: 5, returning: false, slapped: false
        });

        // Hide mobile controls so they don't block
        document.body.classList.add('hide-directions');
    """)
    page.wait_for_timeout(500)
    page.screenshot(path="/app/verification/screenshots/boomerang_falling.png")

    # Wait for it to fall past the bottom and swoop back up
    page.wait_for_timeout(2500)

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
