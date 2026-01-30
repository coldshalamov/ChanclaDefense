import os
import time
from playwright.sync_api import sync_playwright

def test_damage_impact():
    with open('chancla_bomb.html', 'r') as f:
        content = f.read()

    # Expose player
    content = content.replace('const player = {', 'const player = window.player = {')

    # Expose chanclas declaration
    content = content.replace('let chanclas = [];', 'let chanclas = window.chanclas = [];')

    # Prevent reassignment in resetGame
    target = '                chanclas = [];'
    if target not in content:
        print(f"WARNING: Target string '{target}' not found in content.")
    content = content.replace(target, '                chanclas.length = 0;')

    # Expose state
    content = content.replace('const STATE = {', 'const STATE = window.STATE = {')
    content = content.replace('let state = STATE.TITLE;', 'let state = window.state = STATE.TITLE;')

    # Expose resetGame
    content = content.replace('function resetGame() {', 'window.resetGame = function resetGame() {')

    # Hook spawnImpact
    search_str = 'function spawnImpact(x, y, isBig = false, color = null) {'
    replace_str = 'function spawnImpact(x, y, isBig = false, color = null) { console.log("SPAWN_IMPACT:" + JSON.stringify({x, y, isBig, color}));'
    content = content.replace(search_str, replace_str)

    # Debug logs
    content = content.replace('function updateChanclas(dt) {', 'function updateChanclas(dt) { console.log("updateChanclas count:", chanclas.length);')

    temp_file = 'chancla_bomb_test_impact.html'
    with open(temp_file, 'w') as f:
        f.write(content)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            impact_logs = []
            page.on("console", lambda msg: impact_logs.append(msg.text))

            cwd = os.getcwd()
            page.goto('file://' + os.path.join(cwd, temp_file))

            # Start game
            print("Starting game...")
            page.evaluate("() => { window.resetGame(); window.state = window.STATE.PLAYING; }")
            page.wait_for_timeout(1000)

            # Force collision
            print("Forcing collision...")
            page.evaluate("""
                () => {
                    window.chanclas.length = 0;
                    window.chanclas.push({
                        x: window.player.x,
                        y: window.player.y,
                        vx: 0,
                        vy: 0,
                        w: 32,
                        h: 18,
                        type: 'normal',
                        rotation: 0,
                        rotSpeed: 0,
                        slapped: false,
                        isBoomerang: false
                    });
                    console.log("Injected chancla at", window.player.x, window.player.y);
                }
            """)

            # Wait for next frame (impact)
            page.wait_for_timeout(50)
            page.screenshot(path='verification/impact.png')
            print("Screenshot taken: verification/impact.png")

            # Verify logs
            found = False
            for log in impact_logs:
                if "SPAWN_IMPACT" in log and "#ff3333" in log:
                    print("SUCCESS: Found impact with correct color:", log)
                    found = True
                    break

            if not found:
                print("FAILURE: Did not find impact with #ff3333.")
                exit(1)

            browser.close()
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

if __name__ == '__main__':
    test_damage_impact()
