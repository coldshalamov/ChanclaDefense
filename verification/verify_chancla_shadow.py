
from playwright.sync_api import sync_playwright
import time
import os

def verify_chancla_shadow():
    # Read the original file
    with open('chancla_bomb.html', 'r') as f:
        content = f.read()

    # Expose chanclas array
    content = content.replace('let chanclas = [];', 'window.chanclas = [];')

    # Write to temp file
    temp_file = 'chancla_bomb_test.html'
    with open(temp_file, 'w') as f:
        f.write(content)

    cwd = os.getcwd()
    file_url = 'file://' + os.path.join(cwd, temp_file)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(file_url)

        # Inject a stationary chancla
        # We also need to make sure the game loop doesn't immediately move it or clear it.
        # But since we set velocity to 0 and it's within bounds, updateChanclas shouldn't remove it.
        # However, resetGame is called on init.
        # We should probably clear existing chanclas first just in case.
        page.evaluate("""
            window.chanclas = [];
            window.chanclas.push({
                x: 200,
                y: 350,
                vx: 0,
                vy: 0,
                w: 60,
                h: 40,
                type: 'normal',
                rotation: 0,
                rotSpeed: 0,
                slapped: false
            });
        """)

        # Wait a moment for render
        time.sleep(0.5)

        page.screenshot(path='verification/chancla_shadow.png')
        print('Screenshot taken: verification/chancla_shadow.png')

        browser.close()

    # Cleanup
    os.remove(temp_file)

if __name__ == '__main__':
    verify_chancla_shadow()
