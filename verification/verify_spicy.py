from playwright.sync_api import sync_playwright
import time
import os

def verify_spicy_mode():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the game
        cwd = os.getcwd()
        page.goto('file://' + cwd + '/chancla_bomb.html')

        # Start game (click the Play button)
        canvas = page.locator('#game')
        canvas.click(position={'x': 200, 'y': 400})
        time.sleep(1)

        # Set combo to 6 to trigger Spicy Mode
        print("Setting combo count to 6...")
        page.evaluate("window.gameInternals.comboCount = 6")

        # Inject a chancla NEAR player (within slap range but not colliding)
        # Player is at ~630. Slap range 80. Collision ~30.
        # Spawn at y - 60 should be safe.
        print("Injecting chancla...")
        page.evaluate("""
            const p = window.gameInternals.player;
            window.gameInternals.chanclas.push({
                x: p.x, y: p.y - 60, w: 32, h: 18,
                vx: 0, vy: 0,
                type: 'normal', rotation: 0, rotSpeed: 0
            });
        """)

        # Wait for fire particles (and ensure combo persists)
        time.sleep(0.5)

        # Check if combo persisted
        current_combo = page.evaluate("window.gameInternals.comboCount")
        print(f"Current Combo: {current_combo}")

        particles_count = page.evaluate("window.gameInternals.fireParticles.length")
        print(f"Fire particles count: {particles_count}")

        if particles_count > 0:
            print("SUCCESS: Fire particles detected.")
        else:
            print("WARNING: No fire particles detected yet.")

        # Trigger Slap
        print("Triggering slap...")
        page.keyboard.press('Space')

        # Check cooldown immediately
        cooldown = page.evaluate("window.gameInternals.slapCooldown")
        combo = page.evaluate("window.gameInternals.comboCount")
        print(f"Slap Cooldown: {cooldown}")
        print(f"New Combo Count: {combo}")

        # Check if cooldown is reduced (Spicy Mode)
        if 0.0 < cooldown <= 0.12 and combo >= 7:
            print("SUCCESS: Slap hit, combo increased, and cooldown is reduced (Spicy Mode active).")
        else:
            print(f"FAILURE: Cooldown is {cooldown}, expected <= 0.12. Combo is {combo}, expected >= 7")

        # Take screenshot
        page.screenshot(path='verification/spicy_mode.png')
        print("Screenshot saved to verification/spicy_mode.png")

        browser.close()

if __name__ == '__main__':
    verify_spicy_mode()
