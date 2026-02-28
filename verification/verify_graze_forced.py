from playwright.sync_api import sync_playwright
import time
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 450, 'height': 800})
        page = context.new_page()

        cwd = os.getcwd()
        page.goto(f"file://{cwd}/index.html")

        # Wait for canvas
        page.wait_for_selector("#game")

        # Expose internal variables for testing purposes by modifying the DOM
        page.evaluate("""
            const script = document.querySelector('script');
            let content = script.textContent;

            // Expose player and chanclas to window
            content = content.replace('const player = {', 'window.player = {');
            content = content.replace('let chanclas = [];', 'window.chanclas = [];');

            // Re-evaluate the script
            const newScript = document.createElement('script');
            newScript.textContent = content;
            document.body.appendChild(newScript);
        """)

        # Start game by clicking exactly on the Play button
        page.mouse.click(200, 400)
        time.sleep(1)

        # Force a chancla to spawn right next to the player (grazing distance)
        page.evaluate("""
            if(window.chanclas && window.player) {
                window.chanclas.push({
                    x: window.player.x + 60, // 60px away is < 75px graze threshold
                    y: window.player.y,
                    vx: 0,
                    vy: 100, // falling down slowly
                    w: 32,
                    h: 18,
                    type: 'normal',
                    rotation: 0,
                    rotSpeed: 0,
                    slapped: false,
                    grazed: false
                });
            }
        """)

        # Wait a bit for game to process the frame and trigger the graze effect
        time.sleep(0.1)

        page.screenshot(path="verification/graze_forced_test.png")
        print("Screenshot taken.")

        browser.close()

if __name__ == "__main__":
    run()
