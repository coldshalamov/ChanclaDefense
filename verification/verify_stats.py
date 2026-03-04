from playwright.sync_api import sync_playwright
import time
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 450, 'height': 800}) # approximate mobile size
        page = context.new_page()

        cwd = os.getcwd()
        page.goto(f"file://{cwd}/index.html")

        # Wait for canvas
        page.wait_for_selector("#game")

        # Take a screenshot of the title screen to verify the new text and button are there
        time.sleep(1)
        page.screenshot(path="verification/title_screen_with_stats.png")

        # Click the Stats button
        # The Stats button is at y=515 to 561. Center is roughly 538. X is center canvas.
        # Canvas is scaled, but we can click at relative coordinates if we evaluate
        page.evaluate("""
            const evt = new MouseEvent('click', {
                clientX: document.getElementById('game').getBoundingClientRect().width / 2,
                clientY: document.getElementById('game').getBoundingClientRect().height * (538 / 700)
            });
            document.getElementById('game').dispatchEvent(evt);
        """)

        time.sleep(1)
        page.screenshot(path="verification/stats_screen.png")

        browser.close()

if __name__ == "__main__":
    run()
