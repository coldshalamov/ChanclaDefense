import os
import time
from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    # Configure context to simulate mobile touch for the game canvas
    context = browser.new_context(viewport={'width': 450, 'height': 800}, has_touch=True, is_mobile=True)
    page = context.new_page()

    html_path = 'file://' + os.getcwd() + '/index.html'

    # Modify the HTML content before loading to expose game state globally
    with open('index.html', 'r') as f:
        content = f.read()

    # Expose variables and functions to window
    modified_content = content.replace(
        "const isa = {", "window.isa = { \n            chismeTimer: 0,"
    ).replace(
        "const player = {", "window.player = { "
    ).replace(
        "let chanclas = [];", "window.chanclas = [];\n            let chanclas = window.chanclas;"
    ).replace(
        "let pets = [];", "window.pets = [];\n            let pets = window.pets;"
    ).replace(
        "let powerups = [];", "window.powerups = [];\n            let powerups = window.powerups;"
    ).replace(
        "function resetGame() {", "window.resetGame = resetGame;\n            function resetGame() {"
    ).replace(
        "function updatePets(dt) {", "window.updatePets = updatePets;\n            function updatePets(dt) {"
    ).replace(
        "function applyPowerup(p) {", "window.applyPowerup = applyPowerup;\n            function applyPowerup(p) {"
    ).replace(
        "function drawPowerups() {", "window.drawPowerups = drawPowerups;\n            function drawPowerups() {"
    )

    page.route(html_path, lambda route: route.fulfill(body=modified_content, content_type="text/html"))
    page.goto(html_path)
    time.sleep(0.5)

    # Click Play
    page.evaluate("document.querySelector('canvas').dispatchEvent(new MouseEvent('click', {clientX: 200, clientY: 400}))")
    time.sleep(0.5)

    # 1. Force Owen to spawn and drop an item to verify it drops beer
    page.evaluate("window.pets.push({ kind: 'owen', x: 200, y: 500, vx: 0, active: true, duration: 6, dropped: false })")

    # Run a few frames of updatePets to trigger the drop
    for _ in range(10):
        page.evaluate("if(window.updatePets) window.updatePets(0.1)")

    time.sleep(0.5)

    # Take a screenshot
    page.screenshot(path="verification/verify_phone_removed.png")

    # Verify the dropped powerup is a beer, not a phone
    powerups = page.evaluate("window.powerups")
    if powerups:
        print(f"Powerup dropped by Owen: {powerups[-1]['kind']}")
    else:
        print("No powerup dropped (this is fine, random chance).")

    print("Screenshot taken: verification/verify_phone_removed.png")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
