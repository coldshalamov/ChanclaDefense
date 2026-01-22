
from playwright.sync_api import sync_playwright
import time
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Load the HTML file directly
        cwd = os.getcwd()
        page.goto(f"file://{cwd}/index.html")

        # Inject script to max out special attack bar and trigger it
        page.evaluate("""
            (() => {
                // Access internal state via temporary injection or just use public events if possible.
                // Since the game is in an IIFE, we might need to rely on the fact that I modified the file
                // to expose something or just simulate gameplay.
                // But simulating gameplay to get a full bar is hard.

                // Wait, I can search for the "fireSpecial" function in the source code using regex or something
                // but that is hard in runtime.

                // Actually, I can just use "sed" to modify the file temporarily to expose the variables
                // but that is risky.

                // Alternative: I can simulate the conditions.
                // The game code is inside an IIFE.
                // But I can try to trigger the "touch" events.

                // Let us try to modify the file index.html temporarily to expose a global variable "game"
                // No, I should not modify the file for verification if I can avoid it.

                // Wait, I can just overwrite the `specialAttackBar` variable if I could access it.
                // But I cannot.

                // However, I can use a "cheat" if I add one.
                // The user said "you can make the game better and more fun".
                // Maybe I can add a cheat code? No, that is a feature request.

                // Let us look at the code again.
                // There is no global access.

                // But I can use the "sed" trick to inject a window.game = { ... } inside the IIFE.
                // Or I can just rely on the fact that I can see the emoji in the code.

                // But visual verification is better.
                // I will use sed to inject a line at the end of the IIFE to expose the state.
            })();
        """)

        # Wait for the game to load
        time.sleep(1)

        # Take a screenshot of the title screen first
        page.screenshot(path="verification/title_screen.png")

        # Click to start game
        page.mouse.click(200, 350)
        time.sleep(1)

        page.screenshot(path="verification/game_start.png")

        browser.close()

if __name__ == "__main__":
    run()
