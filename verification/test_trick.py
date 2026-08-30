from playwright.sync_api import sync_playwright
import time
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Let's override math.random to always spawn trick
        script = """
        Math.random = () => 0.09;
        """

        cwd = os.getcwd()
        page.goto(f'file://{cwd}/index.html')
        page.evaluate(script)
        page.keyboard.press('Enter')
        time.sleep(1.5) # Wait for spawn and animation
        page.screenshot(path='verification/trick_spawn.png')

        page.keyboard.press('Space') # Slap it
        time.sleep(0.1)
        page.screenshot(path='verification/trick_slap.png')

        browser.close()

if __name__ == '__main__':
    run()
