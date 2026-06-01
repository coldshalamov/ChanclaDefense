from playwright.sync_api import sync_playwright
import os
import glob
import re

def run_cuj(page):
    with open('index.html', 'r') as f:
        content = f.read()

    # Strip IIFE wrapper
    content = re.sub(r'^\s*\(\(\)\s*=>\s*\{\s*', '', content, flags=re.MULTILINE)
    content = re.sub(r'\}\)\(\);\s*$', '', content)

    # Replace variable declarations to make them global so they persist when we write to document
    content = re.sub(r'\blet\s+(state)\b', r'var \1', content)

    with open('verification/temp_test3.html', 'w') as f:
        f.write(content)

    file_url = f"file://{os.path.abspath('verification/temp_test3.html')}"
    page.goto(file_url)

    # Mock localStorage to avoid SecurityError and add coins
    page.evaluate('''
        Object.defineProperty(window, 'localStorage', { value: {
            getItem: () => '{"coins": 9999, "upgrades": {"lives": 0, "shield": 0, "cooldown": 0, "speed": 0, "power": 0}}',
            setItem: () => {}
        }, writable: true });
    ''')

    # Reload with mocked localStorage if needed, or just set state directly
    page.evaluate('''
        window.state = "shop";
        // Force a draw frame
    ''')
    page.wait_for_timeout(500)
    page.screenshot(path="/home/jules/verification/screenshots/verification8.png")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="/home/jules/verification/videos",
            viewport={"width": 400, "height": 700}
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()
            browser.close()
