import re
import os
from playwright.sync_api import sync_playwright

def modify_html_for_test(source_path, target_path):
    with open(source_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Strip the IIFE
    content = re.sub(r'^\s*\(\(.*=>\s*\{\s*', '', content, count=1, flags=re.MULTILINE)
    content = re.sub(r'\}\)\(\);\s*$', '', content, count=1)

    # Convert let to var for global access
    content = re.sub(r'\blet\s+(state|gameData|canvas)\b', r'var \1', content)

    # Give the player a ton of coins to test buying the upgrade
    content = content.replace('coins: 0', 'coins: 5000')

    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(content)

def run_cuj(page):
    temp_html = os.path.abspath('verification/temp_index.html')
    modify_html_for_test('index.html', temp_html)

    # Add a mock for localStorage to prevent SecurityError on file://
    page.add_init_script("Object.defineProperty(window, 'localStorage', { value: { getItem: () => null, setItem: () => {} }, writable: true });")

    file_path = f"file://{temp_html}"
    page.goto(file_path)
    page.wait_for_timeout(1000)

    # Click 'Shop' button (approx y=470 on title screen based on memory)
    page.mouse.click(200, 470)
    page.wait_for_timeout(1000)

    # Take screenshot of the Shop menu to verify UI rendered correctly
    os.makedirs("/app/verification/screenshots", exist_ok=True)
    page.screenshot(path="/app/verification/screenshots/shop_menu.png")
    page.wait_for_timeout(1000)

    # Buy Slap Power (y = 120 + 4 * 95 = 500)
    page.mouse.click(200, 530) # Middle of the power button
    page.wait_for_timeout(1000)

    # Take screenshot after purchase to show decreased coins and leveled up status
    page.screenshot(path="/app/verification/screenshots/shop_menu_bought.png")
    page.wait_for_timeout(500)

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="/app/verification/videos"
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()
            browser.close()

    # Cleanup
    if os.path.exists('verification/temp_index.html'):
        os.remove('verification/temp_index.html')
