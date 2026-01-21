from playwright.sync_api import sync_playwright
import time
import os

def verify_chill_mode():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the game from the file directly using absolute path
        cwd = os.getcwd()
        page.goto('file://' + cwd + '/index.html')

        # Start game by clicking (simulate touch/click)
        canvas = page.locator('#game')
        canvas.click()

        # Wait a bit for game to start
        time.sleep(1)

        # Inject code to trigger "Chill Mode" (simulating beer pickup)
        # We need to access the internal variables. Since they are in an IIFE,
        # we can't access them directly from window.
        # However, for verification of *visuals*, we can modify the code before loading
        # OR we can rely on the fact that I will modify the code to work.

        # Wait! The game variables are inside an IIFE closure.
        # I cannot easily set `slowEffect.timer = 5` from outside without modifying the source
        # or exposing the variables.

        # Strategy: I will rely on the "Chill Mode" implementation to be visually verifying
        # what happens when I *would* have the powerup.
        # But to verify it, I need to trigger it.

        # I will inject a temporary global function or variable exposure in the HTML content
        # if I were modifying the file for testing.
        # But here I am testing the file as is (or will be).

        # Alternative: I can use a sed command to temporarily expose the variable
        # or I can simulate the conditions.
        # Actually, I can just modify the game loop in the browser context? No, closure.

        # Let's use a trick: `sed` to expose `slowEffect` to `window` for testing purposes?
        # Or, since I am editing `index.html` anyway, I could temporarily add `window.game = { slowEffect }`
        # but that's messy.

        # Better approach: The verification script can't easily reach into the closure.
        # However, I can use the `verification` folder to store a modified version of the game
        # or I can just modify `index.html` to be testable.

        # For this task, I will proceed with the implementation and then use a modified verification approach:
        # I will temporarily modify `index.html` (via string replacement in memory or file) to expose the state
        # OR I will just assume I can't easily trigger it without playing.

        # Wait, I can use `sed` to replace `slowEffect = {` with `window.slowEffect = slowEffect = {`
        # in the file before running the test? No, that modifies the file on disk.

        # Let's try to find a way to verify.
        # If I implement the feature correctly, I can verify it by...
        #
        # Actually, for the purpose of this task, I can just write the test to EXPECT to be able to set it,
        # and then I will realize I can't.
        #
        # Let's write a python script that reads index.html, injects a setter, writes to a temp file,
        # and tests that temp file.

        with open('index.html', 'r') as f:
            content = f.read()

        # Inject a way to set slowEffect
        # Locate "const slowEffect =" and replace/append exposure
        content = content.replace('const slowEffect = { timer: 0, factor: 0.62 };',
                                  'const slowEffect = { timer: 0, factor: 0.62 }; window.setChill = () => { slowEffect.timer = 5; };')

        with open('verification/temp_test.html', 'w') as f:
            f.write(content)

        page.goto('file://' + cwd + '/verification/temp_test.html')
        canvas = page.locator('#game')
        canvas.click()
        time.sleep(1)

        # Trigger chill
        page.evaluate('window.setChill()')

        # Wait for render
        time.sleep(0.1)

        page.screenshot(path='verification/chill_mode.png')
        print('Chill mode screenshot taken.')

        browser.close()

        # Clean up
        os.remove('verification/temp_test.html')

if __name__ == '__main__':
    verify_chill_mode()
