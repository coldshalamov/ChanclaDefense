from playwright.sync_api import sync_playwright
import os

def test_trick_chancla():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="/app/verification/videos"
        )
        page = context.new_page()

        # We need to mock the spawn logic to force a trick chancla
        html_path = os.path.abspath('index.html')

        with open(html_path, 'r') as f:
            content = f.read()

        # Expose the internal arrays and make the game start instantly
        content = content.replace("(() => {", "window.gameApp = (() => {")
        content = content.replace("let state = STATE.TITLE;", "let state = STATE.PLAYING;")
        content = content.replace("let chanclas = [];", "let chanclas = [];\n            window.chanclas = chanclas;")

        test_html_path = os.path.abspath('temp_test_trick.html')
        with open(test_html_path, 'w') as f:
            f.write(content)

        page.goto(f"file://{test_html_path}")
        page.wait_for_timeout(500)

        # Inject a trick chancla
        page.evaluate("""() => {
            window.chanclas.push({
                x: 200,
                y: 100,
                vx: 0,
                vy: 200,
                w: 36,
                h: 36,
                type: 'trick',
                rotation: 0,
                rotSpeed: 5,
                slapped: false
            });
        }""")

        # Wait a bit to let it fall
        page.wait_for_timeout(500)

        # Wait more to let it pause and dart
        page.wait_for_timeout(1000)

        page.screenshot(path="/app/verification/screenshots/trick_chancla.png")
        page.wait_for_timeout(1000)

        context.close()
        browser.close()

        if os.path.exists(test_html_path):
            os.remove(test_html_path)

if __name__ == "__main__":
    test_trick_chancla()
