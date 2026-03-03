from playwright.sync_api import sync_playwright
import time
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 450, 'height': 800})
        page = context.new_page()

        cwd = os.getcwd()

        # Inject test function
        with open('index.html', 'r') as f:
            html = f.read()

        injection = """
        window.spawnOwenForce = () => {
            spawnOwen();
        };
        initTitle();
        """
        patched_html = html.rsplit('initTitle();', 1)[0] + injection + html.rsplit('initTitle();', 1)[1]

        with open('test_index_no_taco.html', 'w') as f:
            f.write(patched_html)

        page.goto(f"file://{cwd}/test_index_no_taco.html")

        page.wait_for_selector("#game")
        page.mouse.click(200, 400)
        time.sleep(1)

        page.evaluate("window.spawnOwenForce()")

        time.sleep(3)

        page.screenshot(path="verification/verify_no_taco.png")

        browser.close()

if __name__ == "__main__":
    run()
