import time
import os
from playwright.sync_api import sync_playwright

def verify_dash(page):
    # Construct an absolute file URL for index.html
    html_path = os.path.abspath('index.html')
    file_url = f"file://{html_path}"

    page.goto(file_url)

    # Use evaluate to replace script content before playing
    page.evaluate("""
        () => {
            const scripts = document.querySelectorAll('script');
            scripts.forEach(s => {
                if(s.textContent.includes('function update(dt)')) {
                    const newContent = s.textContent.replace(
                        "const moveLeft = keys.left || touch.left;",
                        "window.player = player; window.dashTrails = dashTrails; window.dashTimer = dashTimer; window.dashCooldown = dashCooldown; window.state = state; const moveLeft = keys.left || touch.left;"
                    );
                    const newScript = document.createElement('script');
                    newScript.textContent = newContent;
                    s.remove();
                    document.body.appendChild(newScript);
                }
            });
        }
    """)

    time.sleep(0.5)

    canvas = page.locator('canvas#game')
    box = canvas.bounding_box()

    play_x = box['x'] + box['width'] / 2
    play_y = box['y'] + (403 / 700) * box['height']

    page.mouse.click(play_x, play_y)

    time.sleep(0.5)

    page.keyboard.press("ArrowRight")
    time.sleep(0.1)
    page.keyboard.press("ArrowRight")

    time.sleep(0.05)

    screenshot_path = 'verification/dash_verification.png'
    page.screenshot(path=screenshot_path)
    print(f"Screenshot saved to {screenshot_path}")

    has_dash_trails = page.evaluate("() => window.dashTrails && window.dashTrails.length > 0")
    print(f"Dash trails active: {has_dash_trails}")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            verify_dash(page)
        finally:
            browser.close()
