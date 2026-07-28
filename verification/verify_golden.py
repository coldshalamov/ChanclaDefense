import re
from playwright.sync_api import sync_playwright

def run_cuj(page):
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Modify to spawn golden chanclas quickly
    content = re.sub(
        r'const isGolden = !isBomb && !isHoming && !isSuper && !isFire && Math\.random\(\) < 0\.05;',
        'const isGolden = true;',
        content
    )

    with open('verification/temp_golden.html', 'w', encoding='utf-8') as f:
        f.write(content)

    page.goto("file:///app/verification/temp_golden.html")
    page.wait_for_timeout(1000)

    # Start game
    page.keyboard.press('Enter')
    page.wait_for_timeout(2000)

    # Take screenshot of the golden chanclas
    page.screenshot(path="/home/jules/verification/screenshots/golden_spawning.png")

    # Try to slap a few
    for _ in range(5):
        page.keyboard.press('Space')
        page.wait_for_timeout(300)

    page.screenshot(path="/home/jules/verification/screenshots/golden_slapped.png")
    page.wait_for_timeout(1000)

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="/home/jules/verification/videos"
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()
            browser.close()
