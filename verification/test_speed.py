import pytest
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 450, 'height': 800})

        import os
        filepath = os.path.abspath('index.html')
        page.goto('file://' + filepath)

        # Test default speed
        page.evaluate("window.setSpecial = (val) => { specialAttackBar = val; specialReadyTriggered = false; };")
        page.evaluate("window.gameData.upgrades.speed = 0")
        page.evaluate("window.resetGame ? window.resetGame() : window.startGameFromTitle()")

        # Move right
        speed_0 = page.evaluate("window.player.speed")
        print(f"Speed level 0: {speed_0}")

        page.evaluate("window.gameData.upgrades.speed = 5")
        page.evaluate("window.resetGame ? window.resetGame() : window.startGameFromTitle()")

        speed_5 = page.evaluate("window.player.speed")
        print(f"Speed level 5: {speed_5}")

        assert speed_5 > speed_0, "Player speed should increase with upgrades"

        browser.close()

if __name__ == "__main__":
    run()
