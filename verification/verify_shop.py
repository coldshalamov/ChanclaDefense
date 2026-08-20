from playwright.sync_api import sync_playwright
import time
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Record video to see the whole interaction if needed
        context = browser.new_context(record_video_dir='/app/verification/videos')
        page = context.new_page()

        cwd = os.getcwd()
        # Create a temporary test file that forces the shop state and gives us coins
        with open('index.html', 'r') as f:
            content = f.read()

        content = content.replace("let state = STATE.TITLE;", "let state = STATE.SHOP;")
        content = content.replace("let gameData = { coins: 0,", "let gameData = { coins: 9999,")

        with open('temp_test.html', 'w') as f:
            f.write(content)

        page.goto(f'file://{cwd}/temp_test.html')
        time.sleep(1) # wait for render
        page.screenshot(path='/app/verification/shop_verification.png')
        browser.close()

if __name__ == '__main__':
    run()
