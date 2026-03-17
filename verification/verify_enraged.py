from playwright.sync_api import sync_playwright
import os
import time

def test_enraged_state():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 450, 'height': 800}, has_touch=True, is_mobile=True)
        page = context.new_page()

        file_path = 'file://' + os.getcwd() + '/index.html'

        with open('index.html', 'r') as f:
            content = f.read()

        content = content.replace('initTitle();\n        })();', 'initTitle();\n        window.isa = isa;\n        window.player = player;\n        window.state = state;\n        window.STATE = STATE;\n        window.chanclas = chanclas;\n        window.spawnChancla = spawnChancla;\n        window.startGameFromTitle = startGameFromTitle;\n        })();')

        page.set_content(content)

        # Click play button exactly
        page.mouse.click(200, 400)

        page.wait_for_timeout(500)

        # Force enraged state
        page.evaluate('''() => {
            window.isa.anger = 20;
            window.isa.enraged = true;
            window.spawnChancla();
        }''')

        page.wait_for_timeout(1000)

        screenshot_path = 'verification/enraged_state.png'
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

        browser.close()

if __name__ == "__main__":
    test_enraged_state()
