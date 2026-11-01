from playwright.sync_api import sync_playwright
import os
import glob

def run_cuj(page):
    # Load the game
    filepath = f"file://{os.path.abspath('index.html')}"
    page.goto(filepath)
    page.wait_for_timeout(500)

    # Click Play
    page.mouse.click(100, 450) # Play button area
    page.wait_for_timeout(500)

    # Expose variables and clear them
    page.evaluate("window.getChanclas = () => window.chanclas;")
    page.evaluate("while(window.chanclas.length > 0) window.chanclas.pop();")

    # Spawn a cactus explicitly
    page.evaluate("""
    const cvs = document.getElementById('game');
    window.chanclas.push({
        x: cvs.width / 2,
        y: cvs.height / 2,
        vx: 0,
        vy: 100,
        w: 34,
        h: 38,
        type: 'cactus',
        rotation: 0,
        rotSpeed: 0,
        sniperTimer: 0
    });
    """)
    page.wait_for_timeout(500)

    # Take screenshot of the cactus
    page.screenshot(path="/tmp/cactus.png")
    page.wait_for_timeout(1000)

if __name__ == "__main__":
    os.makedirs("/tmp/videos", exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="/tmp/videos",
            viewport={"width": 400, "height": 700}
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()
            browser.close()
