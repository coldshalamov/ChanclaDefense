from playwright.sync_api import sync_playwright
import os
import time
import re

def strip_iife(html_path, out_path):
    with open(html_path, 'r') as f:
        content = f.read()

    # Strip the IIFE wrapper
    content = re.sub(r'^\s*\(\(.*=>\s*\{\s*', '', content, flags=re.MULTILINE)
    content = re.sub(r'\}\)\(\);\s*$', '', content, flags=re.MULTILINE)

    # Convert let/const to var for global scope injection
    content = re.sub(r'\b(?:let|const)\s+([a-zA-Z0-9_]+)\b', r'var \1', content)

    # Force gameData.stats.wins to 15 to show Prestige button
    content = content.replace('var gameData = {', 'var gameData = {')
    content = content.replace('if (!gameData.stats.wins) gameData.stats.wins = 1;', 'gameData.stats.wins = 15;')

    with open(out_path, 'w') as f:
        f.write(content)

strip_iife('index.html', 'verification/temp_prestige.html')

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('file://' + os.path.abspath('verification/temp_prestige.html'))

        # Wait for title screen to render
        time.sleep(1)

        # Take a screenshot of the title screen showing the Prestige button
        page.screenshot(path='verification/prestige_title.png')

        # Click the Prestige button (y=620, x=110 to width-110)
        # We can just click in the center of the button
        page.mouse.click(200, 640)
        time.sleep(0.5)

        # Take a screenshot of the Prestige menu
        page.screenshot(path='verification/prestige_menu.png')

        browser.close()

if __name__ == '__main__':
    run()
