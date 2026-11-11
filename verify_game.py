import os
from playwright.sync_api import sync_playwright

def run_test():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        page.on("pageerror", lambda err: print(f"Page error: {err}"))

        file_url = f"file://{os.path.abspath('index.html')}"
        page.goto(file_url)
        page.wait_for_timeout(2000)

        print("Page loaded successfully without crashing.")

        browser.close()

if __name__ == "__main__":
    run_test()
