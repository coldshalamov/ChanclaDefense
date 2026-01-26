from playwright.sync_api import sync_playwright
import time
import os

def verify_cocky():
    # Generate debug file
    with open('index.html', 'r') as f:
        content = f.read()

    # Inject high combo
    debug_content = content.replace('let comboCount = 0;', 'let comboCount = 10;')

    with open('verification/cocky_debug.html', 'w') as f:
        f.write(debug_content)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            cwd = os.getcwd()
            page.goto('file://' + cwd + '/verification/cocky_debug.html')

            # Start game
            canvas = page.locator('#game')
            canvas.click()

            # Wait for game loop
            time.sleep(1)

            # Screenshot
            page.screenshot(path='verification/cocky_state.png')
            print('Cocky state screenshot taken at verification/cocky_state.png')

            browser.close()
    finally:
        # Cleanup
        if os.path.exists('verification/cocky_debug.html'):
            os.remove('verification/cocky_debug.html')

if __name__ == '__main__':
    verify_cocky()
