import os
import time
from playwright.sync_api import sync_playwright

def run_cuj(page):
    html_path = 'file://' + os.path.abspath('index.html')

    # Expose internals
    page.goto(html_path)
    page.evaluate('''() => {
        const scripts = document.querySelectorAll('script');
        let content = scripts[scripts.length - 1].textContent;
        // Make variables global
        content = content.replace('const player = {', 'window.player = {');
        content = content.replace('let chanclas = [];', 'window.chanclas = []; let chanclas = window.chanclas;');
        content = content.replace('let pinatas = [];', 'window.pinatas = []; let pinatas = window.pinatas;');
        content = content.replace('function spawnPowerup(', 'window.spawnPowerup = function(');
        content = content.replace('spawnPowerup(kind', 'window.spawnPowerup(kind');
        content = content.replace('function trySlap()', 'window.trySlap = function()');

        const newScript = document.createElement('script');
        newScript.textContent = content;
        document.body.appendChild(newScript);
    }''')
    page.wait_for_timeout(500)

    # Click canvas to start
    box = page.locator('canvas').bounding_box()
    if box:
        page.mouse.click(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2)
    page.keyboard.press('Enter')
    page.wait_for_timeout(1000)

    # Trigger a taco by evaluating script directly
    page.evaluate('''() => {
        if (window.spawnPowerup) {
            window.spawnPowerup('taco', window.player.x, window.player.y - 150);
            window.chanclas.push({ x: window.player.x - 20, y: window.player.y - 120, vx: 0, vy: 0, w: 30, h: 50, type: 'normal', rotation: 0, rotSpeed: 0, slapped: false });
            window.chanclas.push({ x: window.player.x + 20, y: window.player.y - 120, vx: 0, vy: 0, w: 30, h: 50, type: 'normal', rotation: 0, rotSpeed: 0, slapped: false });
            window.chanclas.push({ x: window.player.x, y: window.player.y - 120, vx: 0, vy: 0, w: 30, h: 50, type: 'normal', rotation: 0, rotSpeed: 0, slapped: false });
        }
    }''')
    page.wait_for_timeout(500)

    # Move player up to grab taco and trigger perfect slaps
    page.keyboard.press('ArrowUp')
    page.wait_for_timeout(1500)
    page.keyboard.up('ArrowUp')
    page.wait_for_timeout(2000)

    page.screenshot(path="/home/jules/verification/screenshots/verification.png")
    page.wait_for_timeout(1000)

if __name__ == "__main__":
    os.makedirs("/home/jules/verification/videos", exist_ok=True)
    os.makedirs("/home/jules/verification/screenshots", exist_ok=True)

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
