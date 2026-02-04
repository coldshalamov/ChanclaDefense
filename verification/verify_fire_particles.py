import os
from playwright.sync_api import sync_playwright

# Path to the game file
game_path = "index.html"
temp_path = "verification/temp_game.html"

# Read the game file
with open(game_path, "r") as f:
    content = f.read()

# Inject code to expose comboCount
# Search for 'let comboCount = 0;'
injection_point = "let comboCount = 0;"
injection_code = """let comboCount = 0;
            window.setCombo = (c) => { comboCount = c; };
            window.spawnFire = () => {
                // Force spawn a bunch
                for(let i=0; i<20; i++) {
                    fireParticles.push({
                            x: player.x + (Math.random() - 0.5) * player.w * 0.7,
                            y: player.y + player.h / 2,
                            vx: (Math.random() - 0.5) * 30,
                            vy: -80 - Math.random() * 120,
                            radius: 6 + Math.random() * 6,
                            color: Math.random() < 0.3 ? '#ffff00' : (Math.random() < 0.6 ? '#ff9900' : '#ff3300'),
                            life: 1.0
                        });
                }
            };
"""

if injection_point in content:
    new_content = content.replace(injection_point, injection_code)
else:
    print("Could not find injection point")
    exit(1)

# Write temp file
with open(temp_path, "w") as f:
    f.write(new_content)

def test_fire_particles():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        url = "file://" + os.path.abspath(temp_path)
        page.goto(url)

        # Start game
        page.click("canvas#game")

        # Set combo to 10 (triggers Fuego mode naturally in update loop)
        page.evaluate("window.setCombo(10)")

        # Also force spawn some immediately for the screenshot to be sure
        page.evaluate("window.spawnFire()")

        # Wait a bit for particles to move up
        page.wait_for_timeout(200)

        screenshot_path = "verification/fire_particles.png"
        page.screenshot(path=screenshot_path)
        print(f"Screenshot taken: {screenshot_path}")

        browser.close()

if __name__ == "__main__":
    test_fire_particles()
