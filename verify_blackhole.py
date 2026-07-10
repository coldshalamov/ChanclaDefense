from playwright.sync_api import sync_playwright
import time
import os
import glob

def run_cuj(page, content):
    # Inject globals
    content = content.replace('initTitle();\n        })();', 'initTitle(); window.spawnTestBH = () => { chanclas.push({x: 200, y: 150, vx: 0, vy: 50, w: 40, h: 40, type: \'blackhole\', rotation: 0, rotSpeed: 1, absorbed: 2}); chanclas.push({x: 250, y: 150, vx: 0, vy: 0, w: 32, h: 18, type: \'normal\', rotation: 0, rotSpeed: 0}); }; window.slapTestBH = () => { player.x = 200; player.y = 200; trySlap(); }; })();')

    with open('/home/jules/verification/temp_bh.html', 'w') as f:
        f.write(content)

    page.goto(f"file:///home/jules/verification/temp_bh.html")
    page.wait_for_selector("#game")

    # Start game
    page.click("#game")
    page.wait_for_timeout(1000)

    # Spawn Blackhole
    page.evaluate("window.spawnTestBH()")
    page.wait_for_timeout(1000)
    page.screenshot(path="/home/jules/verification/screenshots/verification_blackhole.png")

    # Slap Blackhole
    page.evaluate("window.slapTestBH()")
    page.wait_for_timeout(300)
    page.screenshot(path="/home/jules/verification/screenshots/verification_burst.png")
    page.wait_for_timeout(1000)


if __name__ == "__main__":
    os.makedirs("/home/jules/verification/videos", exist_ok=True)
    os.makedirs("/home/jules/verification/screenshots", exist_ok=True)

    cwd = os.getcwd()
    with open(os.path.join(cwd, 'index.html'), 'r') as f:
        content = f.read()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="/home/jules/verification/videos",
            viewport={'width': 450, 'height': 800}
        )
        page = context.new_page()
        try:
            run_cuj(page, content)
        finally:
            context.close()
            browser.close()

    # Print video path
    print(glob.glob("/home/jules/verification/videos/*.webm"))
