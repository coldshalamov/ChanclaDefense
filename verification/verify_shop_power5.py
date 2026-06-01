from playwright.sync_api import sync_playwright
import os
import glob
import re
import time

def run_cuj(page):
    with open('index.html', 'r') as f:
        content = f.read()

    # We will simply serve the original file using python's http server so we can use localStorage!
    # Instead of modifying the file directly, let's just start a simple HTTP server on port 8000
    pass

import threading
import http.server
import socketserver

PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

def start_server():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()

if __name__ == "__main__":
    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()

    time.sleep(1) # give server time to start

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="/home/jules/verification/videos",
            viewport={"width": 400, "height": 700}
        )
        page = context.new_page()
        try:
            page.goto("http://localhost:8000/index.html")
            page.wait_for_timeout(500)

            # Click "Shop / Tienda" which is roughly at (200, 470) on my previous screenshot
            # Actually, using page.mouse.click(200, 480)
            page.mouse.click(200, 480)
            page.wait_for_timeout(1000)

            page.screenshot(path="/home/jules/verification/screenshots/verification5.png")

            # Also click the upgrade button to verify that it works
            # The Slap Power button is the 5th button
            # Let's add some coins first via localStorage
            page.evaluate('''
                let data = JSON.parse(localStorage.getItem('chancla_bomb_save') || '{}');
                data.coins = 9999;
                localStorage.setItem('chancla_bomb_save', JSON.stringify(data));
            ''')

            # Now we just need to re-enter shop or something, or just click it, the button state updates in draw loop
            page.mouse.click(200, 120 + 95*4 + 40) # 5th button center
            page.wait_for_timeout(500)
            page.screenshot(path="/home/jules/verification/screenshots/verification6.png")

        finally:
            context.close()
            browser.close()
