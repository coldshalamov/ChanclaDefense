from playwright.sync_api import sync_playwright
import os
import glob
import re
import time
import threading
import http.server
import socketserver

PORT = 8003
Handler = http.server.SimpleHTTPRequestHandler

def start_server():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()

def run_cuj(page):
    # Actually wait I see the issue. When the page loads it initializes `localStorage.getItem` to `saved`.
    # And it only loads once. If I do page.goto twice, it will load it.
    # But wait! I never set coins to 9999 for the SECOND load!
    # Ah, the second page.goto OVERWRITES the previous page.evaluate changes because localStorage is per origin.
    # So the coins WERE saved to localStorage.

    # Why didn't the click work?
    # Because my click was on (200, 490) but it only highlighted it?
    # Ah! The click events in the code use a `canvas.addEventListener('click', ...)` and use `getMousePos`.
    # But maybe playwright's `mouse.click` is too fast for the browser event loop or something?
    # Let's try mouse.down() then wait then mouse.up() to be sure.

    page.goto(f"http://localhost:{PORT}/index.html")
    page.wait_for_timeout(500)

    page.evaluate('''
        localStorage.setItem('chancla_bomb_save', JSON.stringify({
            coins: 9999,
            upgrades: { lives: 0, shield: 0, cooldown: 0, speed: 0, power: 0 },
            stats: { wins: 1 }
        }));
    ''')

    page.goto(f"http://localhost:{PORT}/index.html")
    page.wait_for_timeout(500)

    page.mouse.down(button="left")
    page.mouse.move(200, 490)
    page.wait_for_timeout(100)
    page.mouse.up(button="left")
    page.wait_for_timeout(1000)

    page.screenshot(path="/home/jules/verification/screenshots/verification13.png")

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
