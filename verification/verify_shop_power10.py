from playwright.sync_api import sync_playwright
import os
import glob
import re
import time
import threading
import http.server
import socketserver

PORT = 8002
Handler = http.server.SimpleHTTPRequestHandler

def start_server():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()

def run_cuj(page):
    # Simply use HTTP server and navigate to it to avoid file:// CORS and localStorage issues
    page.goto(f"http://localhost:{PORT}/index.html")
    page.wait_for_timeout(500)

    # We will override localStorage with lots of coins
    page.evaluate('''
        localStorage.setItem('chancla_bomb_save', JSON.stringify({
            coins: 9999,
            upgrades: { lives: 0, shield: 0, cooldown: 0, speed: 0, power: 0 },
            stats: { wins: 1 }
        }));
    ''')

    # Reload page to apply changes
    page.goto(f"http://localhost:{PORT}/index.html")
    page.wait_for_timeout(500)

    # Click Shop
    # In my verification5.png, click at (200, 480) successfully triggered the highlight state of the button (meaning it was pressed), but it didn't navigate maybe? Or maybe it just needed a moment. Let's try 490.
    # Ah wait, the problem in verification5 is that I took a screenshot before it navigated? Or maybe touch/click bounds on title are different.
    # Looking at the code for title screen:
    # 2690: if (pos.y >= 410 && pos.y <= 460) -> PLAY
    #       if (pos.y >= 470 && pos.y <= 520) -> SHOP
    # So y=490 is perfectly in the middle of SHOP.
    page.mouse.click(200, 490)
    page.wait_for_timeout(1000)

    page.screenshot(path="/home/jules/verification/screenshots/verification11.png")

    # The Slap Power button is the 5th button.
    # y = 120, then +95 for each. 0:120, 1:215, 2:310, 3:405, 4:500. Center is y+40 = 540.
    page.mouse.click(200, 540)
    page.wait_for_timeout(1000)
    page.screenshot(path="/home/jules/verification/screenshots/verification12.png")

if __name__ == "__main__":
    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()
    time.sleep(1)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="/home/jules/verification/videos",
            viewport={"width": 400, "height": 700}
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()
            browser.close()
