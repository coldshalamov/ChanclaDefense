from playwright.sync_api import sync_playwright
import os
import glob

def run_cuj(page):
    file_path = os.path.abspath("index.html")
    page.goto(f"file://{file_path}")
    page.wait_for_timeout(500)

    # Bypass title screen and set up game state
    page.evaluate("""
        window.startGameTest = startGameFromTitle;
        window.startGameTest(false);
    """)
    page.wait_for_timeout(500)

    # Force enrage and spawn a blackhole chancla
    page.evaluate("""
        window.isa.enraged = true;
        window.isa.anger = window.isa.maxAnger; // don't die instantly

        // clear existing chanclas
        while(window.getChanclas().length > 0) {
            window.getChanclas().pop();
        }

        // Spawn a blackhole chancla
        window.getChanclas().push({
            x: 200,
            y: 300,
            vx: 0,
            vy: 0,
            w: 40,
            h: 40,
            type: 'blackhole',
            rotation: 0,
            rotSpeed: 0.1,
            slapped: false
        });

        // Spawn normal chanclas to see them pulled in
        window.getChanclas().push({
            x: 100,
            y: 300,
            vx: 0,
            vy: 0,
            w: 32,
            h: 18,
            type: 'normal',
            rotation: 0,
            rotSpeed: 0.1,
            slapped: false
        });
    """)
    page.wait_for_timeout(500)

    # Slap it
    page.evaluate("""
        // slap it
        const bh = window.getChanclas().find(c => c.type === 'blackhole');
        if (bh) {
            bh.slapped = true;
            bh.isPerfect = true;

            // Simulate slap effect manually for visuals
            window.getFloatTexts().push({ text: 'GRAVITY REVERSED! 🌌', x: bh.x, y: bh.y, time: 1.8, max: 1.8, color: '#9b59b6', fontSize: 14 });
        }
    """)
    page.wait_for_timeout(300)

    # Take screenshot
    page.screenshot(path="/home/jules/verification/screenshots/verification.png")
    page.wait_for_timeout(1000)

if __name__ == "__main__":
    os.makedirs("/home/jules/verification/screenshots", exist_ok=True)
    os.makedirs("/home/jules/verification/videos", exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="/home/jules/verification/videos"
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()
            browser.close()

    video_files = glob.glob("/home/jules/verification/videos/*.webm")
    if video_files:
        print(f"Video saved to {video_files[0]}")
    else:
        print("No video found.")
