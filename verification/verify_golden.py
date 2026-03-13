from playwright.sync_api import sync_playwright
import time
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 450, 'height': 800},
            record_video_dir="verification/video"
        )
        page = context.new_page()

        cwd = os.getcwd()
        page.goto(f"file://{cwd}/index.html")

        # Wait for canvas
        page.wait_for_selector("#game")

        # Inject debug functions to spawn a golden chancla immediately
        content = page.content()
        content = content.replace("initTitle();", """
            initTitle();
            window.spawnGolden = () => {
                const w = 38;
                const h = 22;
                const x = canvas.width / 2;
                const y = isa.y + 40;
                const vy = 150;
                const vx = 0;
                chanclas.push({ x, y, vx, vy, w, h, type: 'golden', rotation: 0, rotSpeed: 0 });
            };
        """)
        page.set_content(content)

        # Start game
        page.mouse.click(200, 400)
        time.sleep(1)

        # Spawn golden chancla
        page.evaluate("window.spawnGolden()")
        time.sleep(1.8) # Wait for it to fall into slap range

        # Slap!
        page.keyboard.press(" ")
        time.sleep(0.1)

        # Take screenshot of the golden slap effect
        page.screenshot(path="verification/golden_slap.png")

        # Wait for the chain reaction / float text
        time.sleep(1)

        context.close()
        browser.close()

if __name__ == "__main__":
    run()
