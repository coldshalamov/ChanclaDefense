from playwright.sync_api import sync_playwright
import os
import time
import threading
import http.server
import socketserver

PORT = 8001
Handler = http.server.SimpleHTTPRequestHandler

def start_server():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()

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
            page.goto("http://localhost:8001/index.html")
            page.wait_for_timeout(500)

            # Click "Shop / Tienda" which is roughly at (200, 470) on my previous screenshot
            # But the click failed to navigate, maybe coordinates are wrong?
            # Let's just mock the mouse click at multiple points around y=470
            page.mouse.click(200, 480)
            page.wait_for_timeout(200)
            page.mouse.click(200, 500)
            page.wait_for_timeout(500)

            page.screenshot(path="/home/jules/verification/screenshots/verification7.png")

        finally:
            context.close()
            browser.close()
