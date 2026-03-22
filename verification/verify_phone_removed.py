import os
import time
from playwright.sync_api import sync_playwright

def verify_phone_removed():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Mobile viewport is crucial for the canvas scaling
        context = browser.new_context(viewport={'width': 450, 'height': 800}, has_touch=True, is_mobile=True)
        page = context.new_page()

        file_path = f"file://{os.path.abspath('index.html')}"

        # Inject state to fast-forward
        page.add_init_script("""
            const mockSave = {
                coins: 9999,
                upgrades: { lives: 5, shield: 1, cooldown: 5, speed: 5 },
                bestScore: 1000,
                stats: { totalSlaps: 100, perfectSlaps: 50, gamesPlayed: 10, totalCoinsEarned: 1000 }
            };
            localStorage.setItem('chancla_bomb_save', JSON.stringify(mockSave));
        """)

        # Start game and expose internals
        page.on("request", lambda request: print(f"Request: {request.url}"))
        page.on("pageerror", lambda err: print(f"Page Error: {err}"))
        page.on("console", lambda msg: print(f"Console: {msg.text}"))

        with open('index.html', 'r') as f:
            content = f.read()

        # Expose internal variables to window object for testing
        content = content.replace("const isa =", "window.isa =")
        content = content.replace("let pets =", "window.pets =")
        content = content.replace("let powerups =", "window.powerups =")
        content = content.replace("function spawnOwen() {", "window.spawnOwen = function() {")
        content = content.replace("function spawnPowerup(kind, x, y) {", "window.spawnPowerup = function(kind, x, y) {")

        # Override the IIFE execution to safely expose variables before game starts
        content = content.replace("initTitle();\n        })();", "window.initTitle = initTitle;\n        })();")

        page.set_content(content)
        page.evaluate("window.initTitle()")

        # Click play button
        page.mouse.click(200, 400)
        time.sleep(0.5)

        # Force spawn an Owen pet to drop powerups
        page.evaluate("window.spawnOwen()")
        time.sleep(0.5) # Wait for pet to spawn

        # Fast forward time to force drops
        for _ in range(10):
             page.evaluate("window.pets.forEach(p => p.dropped = false)")
             time.sleep(0.1)

        # Take a screenshot to show the drops (should only be beer)
        page.screenshot(path="verification/powerups_only_beer.png")

        # Also let's try to manually spawn a phone powerup (should not render the phone but might exist in logic if not fully removed)
        # But since we removed the phone rendering block in drawPowerups, it shouldn't show a phone icon.
        # Actually, let's just make sure there are no errors when the game runs normally.

        # Check if isa object still has chismeTimer
        has_chisme_timer = page.evaluate("window.isa.chismeTimer !== undefined")
        print(f"Isa has chismeTimer: {has_chisme_timer}")

        browser.close()

if __name__ == "__main__":
    verify_phone_removed()
