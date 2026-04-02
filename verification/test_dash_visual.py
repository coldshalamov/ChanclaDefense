import sys
import os
import time
import math
from playwright.sync_api import sync_playwright

def test_dash(page):
    # Get absolute paths to the local files
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    index_path = f"file://{parent_dir}/index.html"
    chancla_path = f"file://{parent_dir}/chancla_bomb.html"

    # Set viewport large enough
    page.set_viewport_size({"width": 800, "height": 900})

    # Test index.html
    page.goto(index_path)

    # Expose variables and state
    page.evaluate("""
        const oldScript = document.querySelector('script').textContent;
        const newScript = oldScript
            .replace('state = STATE.TITLE;', 'state = STATE.PLAYING; window.state = state;')
            .replace('const player = {', 'window.player = {')
            .replace('let chanclas = [];', 'window.chanclas = chanclas; let chanclas_internal = [];')
            .replace('let dashTrails = [];', 'window.dashTrails = dashTrails; let dashTrails_internal = [];');

        // Find the IIFE end and append assignments
        const iifeEndIndex = newScript.lastIndexOf('})();');
        const finalScript = newScript.substring(0, iifeEndIndex) +
            `window.player = player;
             window.dashTrails = dashTrails;
             window.chanclas = chanclas;
            })();` + newScript.substring(iifeEndIndex + 5);

        const scriptTag = document.createElement('script');
        scriptTag.textContent = finalScript;
        document.body.appendChild(scriptTag);
    """)

    # Start game by entering
    page.keyboard.press('Enter')
    page.wait_for_timeout(500)

    # Dash left using Shift key and left arrow
    page.keyboard.down('ArrowLeft')
    page.keyboard.press('Shift')
    page.wait_for_timeout(50) # Let it move slightly and generate trail
    page.keyboard.up('ArrowLeft')

    # Screenshot dash
    page.screenshot(path=f"{current_dir}/dash_screenshot.png")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        try:
            test_dash(page)
        finally:
            browser.close()