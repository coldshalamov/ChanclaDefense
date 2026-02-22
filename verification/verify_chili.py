from playwright.sync_api import sync_playwright
import time
import os

def verify_chili_mode():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        cwd = os.getcwd()
        page.goto('file://' + cwd + '/index.html')

        # Start game by clicking the Play button
        # Canvas size 400x700. Play button is approx y=400.
        canvas = page.locator('#game')
        canvas.click(position={'x': 200, 'y': 400})
        time.sleep(0.5)

        # Trigger Chili Mode using exposed internals
        print("Triggering Chili Mode...")
        page.evaluate("window.gameInternals.player.chiliTimer = 5;")

        # Manually tick the update loop
        print("Manually ticking update loop...")
        for _ in range(60): # Simulate ~1 second
            page.evaluate("window.gameInternals.update(0.016)")

        # Verify state
        chili_timer = page.evaluate("window.gameInternals.player.chiliTimer")
        fire_particles_count = page.evaluate("window.gameInternals.fireParticles.length")

        print(f"Chili Timer: {chili_timer}")
        print(f"Fire Particles Count: {fire_particles_count}")

        if chili_timer < 5 and fire_particles_count > 0:
            print("SUCCESS: Chili Mode active and particles spawned.")
        else:
            print("FAILURE: Chili Mode not active or no particles.")

        # Screenshot
        page.screenshot(path='verification/chili_mode.png')
        print('Screenshot taken: verification/chili_mode.png')

        browser.close()

if __name__ == '__main__':
    verify_chili_mode()
