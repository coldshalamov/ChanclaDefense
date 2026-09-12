import os
import time
from playwright.sync_api import sync_playwright

def verify():
    # Inject a script to force sniper spawn
    test_html = "test_sniper.html"
    with open("index.html", "r") as f:
        content = f.read()

    # Force spawn to be sniper
    content = content.replace(
        "const isSniper = !isBomb && !isHoming && !isSuper && !isGolden && !isBoomerang && !isTrick && Math.random() < 0.10;",
        "const isSniper = true;"
    )
    # Turn off boss movement to make it stable
    content = content.replace(
        "function drawIsa() {",
        "function drawIsa() { isa.x = canvas.width / 2; isa.y = 70;"
    )

    with open(test_html, "w") as f:
        f.write(content)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"file://{os.path.abspath(test_html)}")

        # Start game
        page.keyboard.press("Enter")
        time.sleep(0.5)

        # Give some time for chancla to fall a bit
        time.sleep(1.0)

        page.screenshot(path="verification/sniper.png")

        browser.close()

if __name__ == "__main__":
    verify()
