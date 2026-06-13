import os
import time
from playwright.sync_api import sync_playwright

def verify_suegra():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load and intercept to expose window variables
        def route_handler(route):
            with open("index.html", "r") as f:
                html = f.read()
            # Intercept and expose variables
            html = html.replace('let specialReadyTriggered = false;', 'let specialReadyTriggered = false;\nwindow.getSuegra = () => suegra;\nwindow.getChanclas = () => chanclas;\nwindow.getIsa = () => isa;\nwindow.setSuegraTimer = (v) => { suegraTimer = v; };\nwindow.setIsaEnraged = (v) => { isa.enraged = v; };\nwindow.setPlayerPos = (x, y) => { player.x = x; player.y = y; };\nwindow.trySlapPublic = trySlap;')
            route.fulfill(body=html, content_type="text/html")

        page.route("**/*", route_handler)

        file_path = f"file://{os.path.abspath('index.html')}"
        page.add_init_script("Object.defineProperty(window, 'localStorage', { value: { getItem: () => null, setItem: () => {} }, writable: true });")

        page.goto(file_path)

        # Start game
        page.keyboard.press("Enter")
        time.sleep(0.5)

        page.evaluate("window.setIsaEnraged(true)")
        page.evaluate("window.setSuegraTimer(16)")

        time.sleep(1) # Let update loop catch it and spawn Suegra

        page.evaluate("const s = window.getSuegra(); s.timer = 2.1;")
        time.sleep(0.1) # small sleep to spawn

        # Directly modify slipper to be slapped towards suegra
        suegra_x = page.evaluate("window.getSuegra().x")
        page.evaluate(f"const c = window.getChanclas()[0]; if(c) {{ c.slapped = true; c.x = {suegra_x}; c.y = 40; c.vy = -100; c.type = 'slipper'; }}")

        time.sleep(0.1) # Wait right before it hits or immediately after hit for visual

        page.screenshot(path="verification/suegra_test.png")

        browser.close()

if __name__ == "__main__":
    verify_suegra()
