import re
from playwright.sync_api import sync_playwright

with open("index.html", "r") as f:
    content = f.read()

# Make it spawn only golden chanclas to test
content = content.replace("const isGolden = Math.random() < 0.05;", "const isGolden = true;")

with open("index_test.html", "w") as f:
    f.write(content)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("file:///app/index_test.html")

    # Start game
    page.click("canvas")
    page.wait_for_timeout(500)

    # Wait for chancla to drop
    page.wait_for_timeout(1000)

    page.screenshot(path="golden_chancla.png")

    # Try to slap it
    page.click("canvas")
    page.wait_for_timeout(500)
    page.screenshot(path="golden_chancla_slapped.png")

    browser.close()
