import os
import time
import json
from playwright.sync_api import sync_playwright

def verify_shadow():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Inject script to spy on fillText
        page.add_init_script("""
            const originalFillText = CanvasRenderingContext2D.prototype.fillText;
            CanvasRenderingContext2D.prototype.fillText = function(text, x, y, maxWidth) {
                if (text && (text.includes('🩴'))) {
                    console.log('CHANCLA_SHADOW: ' + JSON.stringify({
                        blur: this.shadowBlur,
                        offsetY: this.shadowOffsetY,
                        color: this.shadowColor
                    }));
                }
                return originalFillText.apply(this, arguments);
            };
        """)

        # Capture console messages
        shadow_data = []
        def on_console(msg):
            if msg.text.startswith('CHANCLA_SHADOW:'):
                try:
                    data = json.loads(msg.text.replace('CHANCLA_SHADOW: ', ''))
                    shadow_data.append(data)
                except Exception as e:
                    print(f"Error parsing JSON: {e}")

        page.on("console", on_console)

        # Load game
        cwd = os.getcwd()
        page.goto('file://' + cwd + '/chancla_bomb.html')

        # Click to start
        canvas = page.locator('#game')
        canvas.click()

        # Wait for chanclas to spawn (approx 1.2s spawn interval)
        print("Waiting for chanclas to spawn...")
        # Need enough time for chancla to appear. Initial spawn is immediate?
        # spawnTimer starts at 0, spawnInterval is 1.2.
        # update() runs. timeElapsed=0.
        # spawnTimer += dt. if spawnTimer >= spawnInterval...
        # So it takes 1.2s to first spawn.
        time.sleep(3)

        browser.close()

        if not shadow_data:
            print("No chanclas drawn detected!")
            # This counts as failure to verify
            exit(1)

        # Check the last frame data
        last_frame = shadow_data[-1]
        print(f"Detected Shadow Data: {last_frame}")

        expected_blur = 8
        expected_offsetY = 4

        # We check if values match target
        if last_frame['blur'] == expected_blur and last_frame['offsetY'] == expected_offsetY:
            print("VERIFICATION RESULT: PASS (Shadow present)")
        else:
            print(f"VERIFICATION RESULT: FAIL (Blur={last_frame['blur']}, OffsetY={last_frame['offsetY']})")

if __name__ == "__main__":
    verify_shadow()
