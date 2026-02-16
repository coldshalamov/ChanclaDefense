
from playwright.sync_api import sync_playwright
import time
import os

def run():
    # 1. Prepare the temporary HTML file with injected code
    with open('chancla_bomb.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Inject exposure of internal variables before the IIFE closes
    # The IIFE closes with `initTitle();\n        })();`
    injection = """
            // TEST INJECTION
            window.getChanclas = () => chanclas;
            window.getPlayer = () => player;
            window.setSpecial = (val) => { specialAttackBar = val; };
            window.fireSpecial = fireSpecialAttack;
            window.spawnChancla = spawnChancla;
            window.forceUpdate = (dt) => update(dt);

            console.log("Test hooks injected");
    """

    # Locate where to inject. Just before the end of the script.
    # The script ends with `initTitle();\n        })();` usually.
    if "initTitle();" in content:
        new_content = content.replace("initTitle();", injection + "\n            initTitle();")
    else:
        print("Could not find initTitle(); to inject code.")
        exit(1)

    with open('temp_chancla_bomb.html', 'w', encoding='utf-8') as f:
        f.write(new_content)

    print("Created temp_chancla_bomb.html with test hooks.")

    # 2. Run Playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Use a mobile-ish viewport
        context = browser.new_context(viewport={'width': 400, 'height': 700})
        page = context.new_page()

        cwd = os.getcwd()
        page.goto(f"file://{cwd}/temp_chancla_bomb.html")

        # Start the game
        page.click("#game")
        time.sleep(1) # Wait for title fade out

        # Setup Test Scenario
        # 1. Set Special to Max
        page.evaluate("window.setSpecial(100)")

        # 2. Spawn a chancla and position it right above the player
        # We need to spawn one and then move it manually to be sure
        page.evaluate("window.spawnChancla()")

        # Move the last chancla to be near player
        page.evaluate("""
            const cs = window.getChanclas();
            const p = window.getPlayer();
            const c = cs[cs.length - 1];
            c.x = p.x;
            c.y = p.y - 100; // 100px above, within 250px range
            c.vx = 0;
            c.vy = 200; // Moving down
            c.slapped = false;
        """)

        print("Scenario setup complete: Chancla above player, Special ready.")

        # Capture state before
        before_vy = page.evaluate("""
            const cs = window.getChanclas();
            cs[cs.length - 1].vy
        """)
        print(f"Chancla VY before: {before_vy}")

        # 3. Fire Special
        page.evaluate("window.fireSpecial()")
        print("Fired Special Attack.")

        # 4. Check results immediately (logic runs synchronously in the function)
        # Verify chancla was slapped and velocity changed
        after_data = page.evaluate("""
            (() => {
                const cs = window.getChanclas();
                const c = cs[cs.length - 1];
                return {
                    vy: c.vy,
                    slapped: c.slapped,
                    isPerfect: c.isPerfect
                };
            })()
        """)

        print(f"Chancla Data after: {after_data}")

        if after_data['vy'] < -100 and after_data['slapped'] == True:
            print("SUCCESS: Chancla was reflected upwards!")
        else:
            print("FAILURE: Chancla was NOT reflected correctly.")
            exit(1)

        # Take screenshot
        page.screenshot(path="verification/special_defense_burst.png")
        print("Screenshot taken.")

        browser.close()

    # Cleanup
    if os.path.exists('temp_chancla_bomb.html'):
        os.remove('temp_chancla_bomb.html')
        print("Cleaned up temp file.")

if __name__ == "__main__":
    run()
