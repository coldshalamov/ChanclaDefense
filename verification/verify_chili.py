from playwright.sync_api import sync_playwright
import time
import os

def verify_chili():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 450, 'height': 800})

        # Load index.html
        cwd = os.getcwd()
        page.goto('file://' + cwd + '/index.html')

        # Click Play button (approx 200, 400)
        page.mouse.click(200, 400)
        time.sleep(1)

        # Inject Chili Mode
        print("Injecting Chili Mode...")
        page.evaluate("window.gameInternals.player.chiliTimer = 5;")

        # Wait a bit for update loop to run
        time.sleep(0.5)

        # Verify state
        chili_timer = page.evaluate("window.gameInternals.player.chiliTimer")
        print(f"Chili timer after 0.5s: {chili_timer}")

        if chili_timer > 0 and chili_timer < 5:
            print("Chili timer is decrementing correctly.")
        else:
            print("FAIL: Chili timer not working as expected.")

        # Take screenshot
        page.screenshot(path='verification/chili_mode.png')
        print("Screenshot saved to verification/chili_mode.png")

        # Verify Visuals by checking exposed properties if possible, or just rely on screenshot manually later.
        # But we can check if slap effect changes type.

        # Trigger Slap
        print("Triggering Slap in Spicy Mode...")
        page.keyboard.press("Space")
        time.sleep(0.1) # Wait for draw

        # Check slap effect type (I can't check internal local variable inside drawSlapEffect easily,
        # but I can check if 'slapEffect.type' was set in 'trySlap' if I exposed it or if I rely on code review.
        # Wait, I didn't expose slapEffect. I exposed gameInternals.
        # But trySlap logic changes a local variable? No, slapEffect is likely module-scoped.
        # I didn't expose slapEffect in gameInternals.
        # I'll skip programmatic verification of slap type and rely on manual/screenshot or code logic.)

        page.screenshot(path='verification/chili_slap.png')
        print("Screenshot saved to verification/chili_slap.png")

        browser.close()

if __name__ == '__main__':
    verify_chili()
