from playwright.sync_api import sync_playwright
import time
import os
import glob

def run_cuj(page):
    cwd = os.getcwd()
    page.goto(f'file://{cwd}/index.html')
    page.wait_for_timeout(500)

    # Calculate precise coordinates relative to the canvas
    canvas = page.locator('#game')
    box = canvas.bounding_box()

    if not box:
        print("Canvas not found!")
        return

    canvas_x = box['x']
    canvas_y = box['y']
    canvas_width = box['width']
    canvas_height = box['height']

    # Click Play (approx relative to original 400x700 scaled)
    play_x = canvas_x + canvas_width / 2
    play_y = canvas_y + (400 / 700) * canvas_height # ~400px down on 700px canvas
    page.mouse.click(play_x, play_y)
    page.wait_for_timeout(500)

    # Send some slaps to try and trigger a rally
    # We will simulate multiple spacebar presses to slap chanclas
    for i in range(15):
        page.keyboard.press(" ")
        page.wait_for_timeout(400)

    page.wait_for_timeout(1000)

    page.screenshot(path="verification/screenshots/rally_verification.png")
    page.wait_for_timeout(1000)

if __name__ == "__main__":
    os.makedirs("verification/screenshots", exist_ok=True)
    os.makedirs("verification/videos", exist_ok=True)

    # Clear old videos
    for f in glob.glob("verification/videos/*.webm"):
        os.remove(f)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="verification/videos",
            viewport={'width': 800, 'height': 800}
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()
            browser.close()
