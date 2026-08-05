from playwright.sync_api import sync_playwright

def verify_greed():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('file:///app/index.html')

        # Click Start
        page.mouse.click(500, 300)

        # Open Shop
        page.mouse.click(500, 500)

        # Scroll not needed, but wait for rendering
        page.wait_for_timeout(500)

        page.screenshot(path='/app/verification/shop_with_greed.png')
        browser.close()

if __name__ == '__main__':
    verify_greed()
