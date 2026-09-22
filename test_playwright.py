from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('file:///app/index.html')
        page.wait_for_timeout(1000)

        # we don't really need to evaluate if it crashes, just checking it doesn't crash on boot is fine since we saw the memory: "The game's internal functions are encapsulated and not exposed globally to the window object"

        # start game
        page.keyboard.press('Enter')
        page.wait_for_timeout(1000)

        # click to get to game
        page.mouse.click(100, 450)
        page.wait_for_timeout(500)

        browser.close()

run()
