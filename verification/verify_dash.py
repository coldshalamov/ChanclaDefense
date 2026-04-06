import os
import time
from playwright.sync_api import sync_playwright

def run_test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Mobile viewport for touch events
        context = browser.new_context(viewport={'width': 400, 'height': 700}, is_mobile=True, has_touch=True)
        page = context.new_page()

        # Determine the absolute path to the local HTML file
        file_path = f"file://{os.path.abspath('index.html')}"
        page.goto(file_path)

        # Allow the game to load
        page.wait_for_timeout(500)

        # Inject script to expose game state for testing
        page.evaluate("""
            window.state = 'playing';
            window.player = {
                x: 200, y: 630, w: 55, h: 45, speed: 230, lives: 3, shield: false, hitTimer: 0,
                dashTimer: 0, dashCooldown: 0, isDashing: false, dashDir: 0, dashSpeed: 800
            };
            window.dashTrails = [];
            window.keys = { left: false, right: false };
            window.triggerDash = function(dir) {
                if (window.player.dashCooldown > 0 || window.player.isDashing) return;
                window.player.isDashing = true;
                window.player.dashDir = dir;
                window.player.dashTimer = 0.15;
                window.player.dashCooldown = 0.8;
                window.player.hitTimer = 0.2;
            };

            // Override update logic for test specifically
            const origUpdate = window.update;
            window.testUpdate = function(dt) {
                if (window.player.isDashing) {
                    window.player.dashTimer -= dt;
                    window.player.x += window.player.dashDir * window.player.dashSpeed * dt;
                    window.dashTrails.push({ x: window.player.x, y: window.player.y, w: window.player.w, h: window.player.h, alpha: 0.6, expression: 'normal' });
                    if (window.player.dashTimer <= 0) {
                        window.player.isDashing = false;
                    }
                }
            };
        """)

        # Press Enter to start game (bypassing touch overlay issues on title screen)
        page.keyboard.press('Enter')
        page.wait_for_timeout(200)

        # Trigger a dash to the right using Shift key simulation
        page.keyboard.down('ArrowRight')
        page.keyboard.press('Shift')
        page.keyboard.up('ArrowRight')

        # Wait a brief moment to allow trails to spawn
        page.wait_for_timeout(80)

        # Take a screenshot while the dash trails are visible
        page.screenshot(path="verification/dash_mechanic.png")
        print("Dash screenshot taken.")

        browser.close()

if __name__ == "__main__":
    run_test()
