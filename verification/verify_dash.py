import os
import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={'width': 450, 'height': 800})
    page = context.new_page()

    content = open('index.html', 'r').read()
    content = content.replace('const player = {', 'window.player = {')
    content = content.replace('let dashTrails = [];', 'window.dashTrails = [];')
    content = content.replace('function startGameFromTitle() {', 'window.startGameFromTitle = function() {')
    content = content.replace('let state = STATE.TITLE;', 'window.state = STATE.TITLE; let state = window.state;')

    # We also need to hook state changes
    content = content.replace('state = STATE.PLAYING;', 'state = STATE.PLAYING; window.state = state;')

    with open('temp_test.html', 'w') as f:
        f.write(content)

    html_path = 'file://' + os.getcwd() + '/temp_test.html'
    page.goto(html_path)

    # Start game
    page.evaluate("window.startGameFromTitle()")
    time.sleep(0.5)

    print("State is:", page.evaluate("window.state"))

    # Move and dash
    page.keyboard.down("ArrowRight")
    time.sleep(0.1)
    page.keyboard.press("Shift")
    time.sleep(0.05)
    page.keyboard.up("ArrowRight")

    dash_active = page.evaluate("window.player.dashTimer > 0 || window.dashTrails.length > 0")
    if dash_active:
        print("SUCCESS: Dash mechanic triggered.")
    else:
        print("FAILURE: Dash did not activate.")
        print("Dash Timer:", page.evaluate("window.player.dashTimer"))
        print("Dash Trails:", page.evaluate("window.dashTrails.length"))

    page.screenshot(path="verification/dash_mechanic.png")
    browser.close()
