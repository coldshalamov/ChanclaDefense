from playwright.sync_api import sync_playwright
import os
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        url = "file://" + os.path.abspath("index.html")

        def handle_route(route):
            with open("index.html", "r") as f:
                content = f.read()

            # Patch the source to simulate slowMoTimer
            content = content.replace("let slowMoTimer = 0;", "let slowMoTimer = 1.5;")

            # To show the text, let's also inject a float text
            content = content.replace("floatTexts = [];", "floatTexts = [{text: 'PERFECT DODGE! 🕒', x: 200, y: 300, time: 2, max: 2}];")

            route.fulfill(body=content, content_type="text/html")

        page.route("**/index.html", handle_route)
        page.goto(url)

        # Start game
        page.click("canvas#game")

        # Wait a bit for the game to update
        time.sleep(0.5)

        page.screenshot(path="verification/perfect_dodge_visual.png")
        print("Screenshot taken: verification/perfect_dodge_visual.png")
        browser.close()

if __name__ == "__main__":
    run()
