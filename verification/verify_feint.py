import os
import time
from playwright.sync_api import sync_playwright

def verify_feint():
    print("Preparing test...")
    # 1. Create a test version of the game with 100% feint rate
    with open('chancla_bomb.html', 'r') as f:
        content = f.read()

    # Replace the probability line to force feint
    test_content = content.replace(
        "const isFeint = !isSuper && Math.random() < 0.1;",
        "const isFeint = true;"
    )

    # Expose chanclas array via getter
    test_content = test_content.replace(
        "initTitle();",
        "window.getChanclas = () => chanclas; initTitle();"
    )

    with open('chancla_bomb_test.html', 'w') as f:
        f.write(test_content)

    try:
        with sync_playwright() as p:
            print("Launching browser...")
            browser = p.chromium.launch()
            page = browser.new_page()

            # Load the test file
            abs_path = os.path.abspath('chancla_bomb_test.html')
            url = f'file://{abs_path}'
            print(f"Loading {url}...")
            page.goto(url)

            # Start game by clicking canvas
            print("Clicking canvas to start game...")
            page.click('#game')

            print("Game started. Waiting for chanclas...")

            # Wait for a chancla to be spawned
            page.wait_for_function("() => window.getChanclas() && window.getChanclas().length > 0")

            # Wait for the feint state (state 1 is pause)
            # We poll for a chancla in state 1
            print("Waiting for feint pause (state 1)...")
            try:
                page.wait_for_function("""() => {
                    const c = window.getChanclas()[0];
                    return c && c.feintState === 1;
                }""", timeout=10000)
                print("Confirmed: Chancla entered Feint Pause state.")
            except Exception as e:
                print(f"Error waiting for pause: {e}")
                # Dump state
                chanclas = page.evaluate("window.getChanclas()")
                print(f"Chanclas state: {chanclas}")
                raise e

            # Check velocity is 0 during pause
            vx, vy = page.evaluate("""() => {
                const c = window.getChanclas()[0];
                return [c.vx, c.vy];
            }""")
            print(f"Velocity during pause: vx={vx}, vy={vy}")

            # Approximate check for float 0
            if abs(vx) > 0.1 or abs(vy) > 0.1:
                print("FAILURE: Velocity should be ~0 during pause!")
                exit(1)
            else:
                print("SUCCESS: Velocity is 0 during pause.")

            # Wait for resume (state 2)
            print("Waiting for feint strike (state 2)...")
            page.wait_for_function("""() => {
                const c = window.getChanclas()[0];
                return c && c.feintState === 2;
            }""", timeout=5000)
            print("Confirmed: Chancla entered Feint Strike state.")

            # Check velocity is high
            vy_new = page.evaluate("window.getChanclas()[0].vy")
            print(f"Velocity after resume: {vy_new}")

            if vy_new < 100: # Should be fast
                print("FAILURE: Velocity too low after resume!")
                exit(1)
            else:
                print("SUCCESS: Velocity increased after resume.")

            page.screenshot(path="verification/feint_verified.png")
            print("Verification screenshot saved to verification/feint_verified.png")

            browser.close()

    finally:
        # Cleanup
        if os.path.exists('chancla_bomb_test.html'):
            os.remove('chancla_bomb_test.html')

if __name__ == "__main__":
    verify_feint()
