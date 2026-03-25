from playwright.sync_api import Page, expect, sync_playwright
import os
import time

def verify_cosmetics_menu(page: Page):
    # Setup for local file testing
    file_path = f"file://{os.path.abspath('chancla_bomb.html')}"

    # Expose global variables to manipulate state easily
    with open('chancla_bomb.html', 'r') as f:
        content = f.read()

    content = content.replace(
        "initTitle();\n        })();",
        "initTitle();\n        window.gameData = gameData;\n        window.saveGameData = saveGameData;\n        window.STATE = STATE;\n        window.state = state;\n        })();"
    )

    page.set_content(content)

    # Set high coins so we can buy hats
    page.evaluate("gameData.coins = 1000; saveGameData();")

    # Click the "Hats / Gorras" button on the title screen
    # Its coordinates are roughly: y >= 590 && y <= 636, x >= 110

    # Since we modified the HTML string and used set_content, canvas sizing might be slightly different than goto.
    # It's safer to just set the state directly for the screenshot to guarantee we see the menu.
    page.evaluate("state = STATE.COSMETICS;")

    # Wait for the next animation frame to draw the menu
    time.sleep(0.5)

    page.screenshot(path="verification/cosmetics_menu_unpurchased.png")

    # Click the "Sombrero" buy button
    # y = 130 + 75 (Sombrero is second item) = 205
    # pos.y >= 205 && pos.y <= 270, pos.x >= 30
    rect = page.evaluate("document.getElementById('gameCanvas').getBoundingClientRect()")
    page.mouse.click(rect['left'] + 100, rect['top'] + 230)

    time.sleep(0.5)
    page.screenshot(path="verification/cosmetics_menu_purchased.png")

    # Go to play state to see the hat
    page.evaluate("state = STATE.PLAYING;")
    time.sleep(0.5)
    page.screenshot(path="verification/player_with_sombrero.png")


if __name__ == "__main__":
    with sync_playwright() as p:
        # Set viewport explicitly for the mobile canvas
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 450, 'height': 800})
        page = context.new_page()
        try:
            verify_cosmetics_menu(page)
        finally:
            browser.close()
