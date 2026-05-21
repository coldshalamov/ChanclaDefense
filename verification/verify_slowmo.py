from playwright.sync_api import sync_playwright
import time
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        file_path = os.path.abspath('index.html')
        content = open(file_path).read()

        # Modify IIFE to expose variables
        content = content.replace('const player = {', 'window.player = {')
        content = content.replace('let chanclas = [];', 'window.chanclas = []; let chanclas = window.chanclas;')
        content = content.replace('let slowMoTimer = 0;', 'window.getSlowMoTimer = () => slowMoTimer; let slowMoTimer = 0;')
        content = content.replace('let dashTimer = 0;', 'window.getDashTimer = () => dashTimer; let dashTimer = 0;')
        content = content.replace('let state = STATE.TITLE;', 'let state = STATE.PLAYING; window.state = state;')

        page.route('**/*', lambda route: route.fulfill(body=content, content_type="text/html") if route.request.url.endswith('index.html') else route.continue_())
        page.goto('file://' + file_path)

        time.sleep(1) # Wait for init

        # Double tap ArrowRight
        page.keyboard.press('ArrowRight')
        page.keyboard.up('ArrowRight')
        time.sleep(0.05)
        page.keyboard.press('ArrowRight')
        page.keyboard.up('ArrowRight')

        time.sleep(0.05) # Wait for dash trigger

        # Spawn chancla during dash to trigger perfect dodge
        page.evaluate('''
            const p = window.player;
            window.chanclas.push({
                x: p.x,
                y: p.y,
                vx: 0,
                vy: 0,
                w: 32,
                h: 18,
                type: 'normal',
                rotation: 0,
                rotSpeed: 0,
                slapped: false
            });
        ''')

        time.sleep(0.1) # Wait for game loop to process collision and set cyan background

        slow_mo = page.evaluate('window.getSlowMoTimer()')
        dodged = page.evaluate('window.chanclas[0] ? window.chanclas[0].dodged : false')

        print(f"Dodged: {dodged}, SlowMoTimer: {slow_mo}")

        page.screenshot(path="verification/perfect_dodge_slowmo.png")
        print("Screenshot saved to verification/perfect_dodge_slowmo.png")

        browser.close()

if __name__ == '__main__':
    run()
