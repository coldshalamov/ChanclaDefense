from playwright.sync_api import sync_playwright
import os
import time
import re

def verify_prestige_ui():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Mock localStorage to avoid SecurityError for file://
        page.add_init_script("Object.defineProperty(window, 'localStorage', { value: { getItem: () => null, setItem: () => {} }, writable: true });")

        # Read the file and bypass IIFE to expose state
        with open('index.html', 'r') as f:
            content = f.read()
        content = re.sub(r'^\s*\(\(.*=>\s*\{\s*', '', content)
        content = re.sub(r'\}\)\(\);\s*$', '', content)
        content = re.sub(r'\blet\s+(state|gameData|canvas|ctx|fiestaMode|fiestaHue|hitStop|dashTrails)\b', r'var \1', content)

        # Force prestige condition
        content = content.replace("let gameData = {", "var gameData = { prestige: 2,")
        content = content.replace("if (!gameData.stats.wins) gameData.stats.wins = 1;", "gameData.stats.wins = 15;\nif (!gameData.stats.wins) gameData.stats.wins = 1;")

        temp_file = os.path.abspath('verification/temp_prestige.html')
        with open(temp_file, 'w') as f:
            f.write(content)

        page.goto('file://' + temp_file)

        # Take a screenshot of the Title screen (which should now show Prestige)
        time.sleep(0.5)
        page.screenshot(path='verification/prestige_title.png')
        print("Prestige title screenshot taken.")

        # Click the prestige button (y=620)
        page.mouse.click(200, 640)
        time.sleep(0.5)
        page.screenshot(path='verification/prestige_menu.png')
        print("Prestige menu screenshot taken.")

        browser.close()

if __name__ == '__main__':
    verify_prestige_ui()
