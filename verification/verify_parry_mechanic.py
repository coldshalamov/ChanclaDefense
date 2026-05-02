from playwright.sync_api import sync_playwright
import os

def run_cuj(page):
    # Get absolute path for the index.html
    current_dir = os.path.dirname(os.path.abspath(__file__))
    target_path = os.path.abspath(os.path.join(current_dir, '../index.html'))

    # Load game using file:// protocol
    page.goto(f"file://{target_path}")
    page.wait_for_timeout(500)

    # Inject debug script to manipulate state
    page.evaluate('''() => {
        window.Math.random = () => 0.1; // Force parry chance
        state = 'playing'; // force playing state
        window.state = state;
    }''')

    # Hit enter to start
    page.keyboard.press("Enter")
    page.wait_for_timeout(500)

    # Wait for the first chancla to hit Isa
    page.wait_for_timeout(2000)

    # Take screenshot at the key moment of the parry
    page.screenshot(path="verification/screenshots/verification.png")
    page.wait_for_timeout(2000)

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="verification/videos",
            viewport={"width": 500, "height": 800}
        )
        page = context.new_page()
        try:
            run_cuj(page)
        except Exception as e:
            print("Error during test:", e)
        finally:
            context.close()
            browser.close()
