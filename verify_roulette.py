from playwright.sync_api import sync_playwright
import os

def verify_roulette(page):
    page.goto(f"file://{os.path.abspath('index.html')}")
    # Start game
    page.mouse.click(200, 350)
    page.wait_for_timeout(500)

    # Let script play out for 10 seconds to generate chanclas organically, hopefully we see a roulette one
    page.wait_for_timeout(10000)
    page.screenshot(path="verification_roulette.png")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Record video
        context = browser.new_context(
            viewport={"width": 400, "height": 700},
            record_video_dir="videos/"
        )
        page = context.new_page()
        page.add_init_script("""
            localStorage.setItem('chancla_bomb_save', JSON.stringify({
                stats: { wins: 0 },
                upgrades: { lives: 0, shield: 0, cooldown: 0, speed: 0, power: 0, greed: 0 }
            }));
        """)

        try:
            verify_roulette(page)
            # wait before closing to hold screen state for video
            page.wait_for_timeout(1000)
        finally:
            context.close()
            browser.close()
