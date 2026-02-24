from playwright.sync_api import sync_playwright
import os
import time

def verify_curve_chancla():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        cwd = os.getcwd()
        page.goto('file://' + cwd + '/index.html')

        # Start game by clicking Play button (approx x=200, y=400 on 400x700 canvas)
        # Canvas might be scaled, but click(position=...) works in CSS pixels of the element
        # The game logic uses relative coordinates.
        # Let's try clicking slightly lower than center.
        # Play button is at y=380 to 426. Canvas height 700. Center is 350.
        # So y=400 is good.
        page.locator('#game').click(position={'x': 200, 'y': 400})
        time.sleep(1) # Wait for game to start

        # Enable force curve (assuming implementation supports it)
        page.evaluate("window.forceCurve = true")

        # Spawn a chancla explicitly
        page.evaluate("window.gameInternals.spawnChancla()")

        # Wait a frame or two for render
        time.sleep(0.1)

        # Check for curve type
        chanclas = page.evaluate("window.gameInternals.chanclas")
        curve_found = False
        for c in chanclas:
            if c.get('type') == 'curve':
                curve_found = True
                print(f"Found curve chancla at x={c['x']}, y={c['y']}")
                break

        if curve_found:
            print("SUCCESS: Curve chancla spawned.")
        else:
            print("FAILURE: No curve chancla found.")
            print("Chanclas:", chanclas)
            exit(1)

        page.screenshot(path='verification/curve_chancla.png')
        browser.close()

if __name__ == "__main__":
    verify_curve_chancla()
