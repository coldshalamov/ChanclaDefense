import os
import time
from playwright.sync_api import sync_playwright

def create_test_file():
    with open("chancla_bomb.html", "r", encoding="utf-8") as f:
        content = f.read()

    # Inject debug hook before the end of the IIFE
    # The IIFE ends with "})();"
    # We want to expose variables.

    # We can inject a function that we can call from outside.
    # We'll search for "initTitle();" which is at the end, and add our hook before it.

    hook_code = """
            // DEBUG HOOK
            window.debugGame = {
                setCombo: (c) => { comboCount = c; },
                spawnTestChancla: () => {
                   chanclas.push({ x: player.x, y: player.y - 40, vx: 0, vy: 0, w: 32, h: 18, type: 'normal', rotation: 0, rotSpeed: 0 });
                },
                triggerSlap: () => {
                    trySlap();
                },
                getChanclas: () => chanclas,
                getIsa: () => isa
            };
            state = STATE.PLAYING; // Force playing state
    """

    new_content = content.replace("initTitle();", hook_code + "\n            initTitle();")

    with open("chancla_bomb_test.html", "w", encoding="utf-8") as f:
        f.write(new_content)

def verify_fuego():
    create_test_file()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        url = "file://" + os.path.abspath("chancla_bomb_test.html")
        page.goto(url)

        # Wait for game to load
        page.wait_for_selector("canvas#game")

        # Verify debug hook exists
        page.wait_for_function("window.debugGame !== undefined")

        print("Debug hook loaded.")

        # Set combo to 6
        page.evaluate("window.debugGame.setCombo(6)")

        # Spawn test chancla close to player
        page.evaluate("window.debugGame.spawnTestChancla()")

        # Verify chancla spawned
        chanclas = page.evaluate("window.debugGame.getChanclas()")
        assert len(chanclas) > 0, "Chancla should have spawned"
        print("Test chancla spawned.")

        # Trigger Slap
        page.evaluate("window.debugGame.triggerSlap()")

        # Verify chancla became Fire
        chanclas = page.evaluate("window.debugGame.getChanclas()")
        assert len(chanclas) > 0, "Chancla should still exist (slapped away)"
        fuego_chancla = chanclas[-1] # Should be the last one we added and slapped

        print(f"Chancla props: slapped={fuego_chancla.get('slapped')}, isFire={fuego_chancla.get('isFire')}")

        assert fuego_chancla.get('slapped') == True, "Chancla should be slapped"
        assert fuego_chancla.get('isFire') == True, "Chancla should be Fuego (isFire=true)"

        print("SUCCESS: Fuego Chancla logic verified.")

        # Take screenshot
        page.screenshot(path="verification/fuego_chancla.png")
        print("Screenshot saved to verification/fuego_chancla.png")

        browser.close()

if __name__ == "__main__":
    verify_fuego()
