from playwright.sync_api import sync_playwright, expect
import os
import time

def test_combo_breaker():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the debug game
        url = "file://" + os.path.abspath("chancla_bomb_debug.html")
        page.goto(url)

        # Start game
        page.evaluate("window.debugGame.startGame()")
        time.sleep(1) # Wait for start

        # Set high combo
        page.evaluate("window.debugGame.setCombo(10)")

        # Verify combo is high (we can't easily check internal var without getter, but we can check HUD if we parsed it)
        # Instead, we just trust the setter and trigger the hit.

        # Trigger hit
        page.evaluate("window.debugGame.forceHit()")

        # Wait for collision logic to run (next frame)
        time.sleep(0.5)

        # Get dialogue text
        dialogue = page.evaluate("window.debugGame.getDialogue()")
        print(f"Dialogue after hit: {dialogue}")

        # Expected lines
        expected_lines = [
            "¡Te sentías muy salsa, eh?",
            "Iba bien... hasta que llegué yo. 😏",
            "¿Te pusiste nervioso, papi?",
            "Rompiendo tu combo y tu corazón. 💔"
        ]

        if dialogue in expected_lines:
            print("SUCCESS: Combo Breaker dialogue triggered!")
        else:
            print(f"FAILURE: Unexpected dialogue '{dialogue}'")
            # It might be low health dialogue if lives dropped to 1?
            # Start lives is 3. 1 hit -> 2 lives. Should be combo breaker.

        # Take screenshot
        page.screenshot(path="verification/combo_breaker_test.png")

        browser.close()

if __name__ == "__main__":
    test_combo_breaker()
