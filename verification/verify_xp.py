from playwright.sync_api import sync_playwright
import time
import os

def verify_xp():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the game
        cwd = os.getcwd()
        page.goto('file://' + cwd + '/chancla_bomb.html')

        # Wait for load
        page.wait_for_timeout(1000)

        # Set XP to 499 (Level 1, needs 500 total)
        print("Setting XP to 499...")
        page.evaluate('window.gameInternals.setXP(499, 1)')

        # Start game manually to ensure state is correct
        print("Starting game...")
        page.evaluate('window.gameInternals.resetGame()')

        # Manually step
        page.evaluate('window.gameInternals.update(0.1)')

        # Inject chancla below screen to score points
        print("Injecting scoring chancla...")
        page.evaluate('''
            window.gameInternals.chanclas.push({
                x: 10, y: 750, w: 30, h: 30, vx: 0, vy: 100, type: "normal", rotation: 0, rotSpeed: 0
            })
        ''')
        # Step update to process score
        page.evaluate('window.gameInternals.update(0.1)')

        score = page.evaluate('window.gameInternals.getScore()')
        print(f"Current Score: {score}")

        # Now kill the player
        print("Killing player...")
        page.evaluate('window.gameInternals.player.lives = 1')
        page.evaluate('''
            window.gameInternals.chanclas.push({
                x: window.gameInternals.player.x,
                y: window.gameInternals.player.y,
                w: 30, h: 30, vx: 0, vy: 0, type: "normal", rotation: 0, rotSpeed: 0
            })
        ''')

        # Step update to process hit
        page.evaluate('window.gameInternals.update(0.1)')

        # Verify Level Up
        level = page.evaluate('window.gameInternals.gameData.streetLevel')
        print(f"Current Level: {level}")

        if level == 2:
            print("SUCCESS: Level increased to 2!")
        else:
            print(f"FAILURE: Level is {level}, expected 2.")
            cred = page.evaluate('window.gameInternals.gameData.streetCred')
            print(f"Current Cred: {cred}")

        # Screenshot
        page.screenshot(path='verification/levelup.png')
        print("Screenshot taken: verification/levelup.png")

        browser.close()

if __name__ == '__main__':
    verify_xp()
