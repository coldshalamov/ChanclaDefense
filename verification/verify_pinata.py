from playwright.sync_api import sync_playwright
import os

def test_pinata(page):
    filepath = 'file://' + os.path.abspath('index.html')
    page.goto(filepath)

    # We need to expose state and override the random chance to force a pinata spawn
    # Let's extract the script content, modify it to spawn a pinata, and inject it
    content = page.content()

    # Simple trick: just run some JS in the page context to start the game and spawn a pinata.
    # We can use keyboard to start
    page.keyboard.press('Enter')
    page.wait_for_timeout(100)

    # We need access to spawnPinata. Since it's inside an IIFE, we can't call it directly.
    # However, we can patch the html in memory for this test specifically.

    html = open('index.html').read()

    # Make spawnPinata global
    html = html.replace('function spawnPinata()', 'window.spawnPinata = function()')

    with open('verification/temp_pinata.html', 'w') as f:
        f.write(html)

    page.goto('file://' + os.path.abspath('verification/temp_pinata.html'))
    page.keyboard.press('Enter')
    page.wait_for_timeout(500)

    # Now call it
    page.evaluate('window.spawnPinata()')

    # Wait for it to fall down a bit
    page.wait_for_timeout(200)

    page.screenshot(path='verification/pinata_screenshot.png')

    # Hit it 3 times to see confetti
    # The slap radius is 80, centered on player.
    # We can just simulate slaps repeatedly while it falls.
    for _ in range(30):
        page.keyboard.press('Space')
        page.wait_for_timeout(50)

    page.screenshot(path='verification/pinata_break_screenshot.png')

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Use mobile viewport to ensure canvas scaling matches tests
        context = browser.new_context(
            viewport={'width': 375, 'height': 812},
            is_mobile=True,
            has_touch=True
        )
        page = context.new_page()
        try:
            test_pinata(page)
        finally:
            browser.close()
