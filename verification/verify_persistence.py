
import os
import time
from playwright.sync_api import sync_playwright

def verify_persistence():
    # 1. Prepare the test file with injected helpers
    # Read from repo root
    html_path = os.path.abspath('chancla_bomb.html')
    with open(html_path, 'r') as f:
        content = f.read()

    # Inject helpers to expose internal state
    # We replace the end of the IIFE to add global functions
    # The IIFE ends with `})();` followed by `</script>`.

    injection = """
            window.getBestScore = () => bestScore;
            window.setScore = (s) => score = s;
            window.triggerEndGame = () => endGame();
        })();
    """

    if "})();" in content:
        # Split by the last occurrence of })(); to be safe
        parts = content.rsplit("})();", 1)
        if len(parts) == 2:
            new_content = parts[0] + injection + parts[1]
        else:
             print("Error: Could not split IIFE properly.")
             return
    else:
        print("Error: Could not find IIFE closing tag to inject code.")
        return

    # Write to a temporary file in the verification directory
    test_file_path = os.path.abspath('verification/chancla_bomb_test.html')
    with open(test_file_path, 'w') as f:
        f.write(new_content)

    file_url = 'file://' + test_file_path
    print(f"Testing URL: {file_url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        print("\nStep 1: Verify initial state (empty storage)")
        page.goto(file_url)
        # Wait for game to initialize
        page.wait_for_function("typeof window.getBestScore === 'function'")

        best = page.evaluate("window.getBestScore()")
        print(f"Initial Best Score: {best}")
        assert best == 0, f"Best score should be 0 initially, got {best}"

        print("\nStep 2: Inject High Score into localStorage and reload")
        page.evaluate("localStorage.setItem('chanclaBombHighScore', '12345')")
        page.reload()
        page.wait_for_function("typeof window.getBestScore === 'function'")

        best = page.evaluate("window.getBestScore()")
        print(f"Loaded Best Score: {best}")
        assert best == 12345, f"Best score should be 12345, got {best}"

        # Take screenshot to verify Title Screen display
        time.sleep(1)
        page.screenshot(path='verification/high_score_title.png')
        print("Screenshot taken: verification/high_score_title.png")

        print("\nStep 3: Simulate Game Over with new High Score")
        # Set a new high score that beats the current one
        new_high = 50000
        page.evaluate(f"window.setScore({new_high})")

        # Trigger game over
        page.evaluate("window.triggerEndGame()")

        # Wait a moment for localStorage update (it's synchronous but good practice)
        time.sleep(0.1)

        # Verify localStorage is updated
        stored = page.evaluate("localStorage.getItem('chanclaBombHighScore')")
        print(f"Stored High Score in localStorage: {stored}")
        assert str(stored) == str(new_high), f"localStorage should have {new_high}, got {stored}"

        # Also check internal bestScore variable
        internal_best = page.evaluate("window.getBestScore()")
        print(f"Internal Best Score variable: {internal_best}")
        assert internal_best == new_high, f"Internal bestScore should be {new_high}, got {internal_best}"

        print("\nVerification Successful!")
        browser.close()

    # Cleanup
    if os.path.exists(test_file_path):
        os.remove(test_file_path)

if __name__ == '__main__':
    verify_persistence()
