from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 450, 'height': 800})
        page = context.new_page()

        cwd = os.getcwd()
        page.goto(f"file://{cwd}/index.html")

        # Wait for canvas
        page.wait_for_selector("#game")

        # Dispatch touchstart to the stats button area
        page.evaluate('''
            const canvas = document.getElementById('game');
            const rect = canvas.getBoundingClientRect();
            // Stats button bounds: 110, 500, canvas.width - 220, 46
            // We'll click at center x (200), y (520)
            // But we need to scale to client rect
            const scaleY = rect.height / canvas.height;
            const clientY = rect.top + 520 * scaleY;

            const event = new TouchEvent('touchstart', {
                bubbles: true,
                cancelable: true,
                touches: [new Touch({
                    identifier: 0,
                    target: canvas,
                    clientX: rect.left + rect.width / 2,
                    clientY: clientY
                })]
            });
            canvas.dispatchEvent(event);
        ''')

        # Wait a bit
        page.wait_for_timeout(500)

        # Take screenshot of the Stats screen
        page.screenshot(path="verification/stats_screen.png")

        browser.close()

if __name__ == "__main__":
    run()
