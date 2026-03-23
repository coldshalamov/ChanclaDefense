from playwright.sync_api import sync_playwright
import os

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    # Configure context to simulate mobile touch if needed, or just specific viewport
    context = browser.new_context(viewport={'width': 450, 'height': 800}, has_touch=True, is_mobile=True)
    page = context.new_page()

    # Create dummy local storage data to show progress
    init_script = """
    localStorage.setItem('chancla_bomb_save', JSON.stringify({
        coins: 100,
        upgrades: {lives: 0, shield: 0, cooldown: 0, speed: 0},
        bestScore: 250,
        stats: {totalSlaps: 150, perfectSlaps: 15, gamesPlayed: 5, totalCoinsEarned: 200},
        achievements: {'first_blood': true}
    }));
    """
    page.add_init_script(init_script)

    file_url = 'file://' + os.path.abspath('index.html')
    page.goto(file_url)

    # Wait for canvas to load
    page.wait_for_selector('canvas#game')

    # Take a screenshot of the Title Screen
    page.screenshot(path='verification/title_screen.png')

    # Calculate coordinates for the Achievements button on Title Screen
    # The button is at y=495-535, x=110 to width-110
    # Canvas is scaled, so we should click relatively, or just use page.evaluate
    page.evaluate('''() => {
        const canvas = document.getElementById('game');
        const rect = canvas.getBoundingClientRect();
        const scaleY = rect.height / canvas.height;
        const scaleX = rect.width / canvas.width;

        // Dispatch synthetic click at Achievements button (center: x=200, y=515)
        const clientX = rect.left + 200 * scaleX;
        const clientY = rect.top + 515 * scaleY;

        const event = new MouseEvent('click', {
            view: window,
            bubbles: true,
            cancelable: true,
            clientX: clientX,
            clientY: clientY
        });
        canvas.dispatchEvent(event);
    }''')

    page.wait_for_timeout(500)

    # Take screenshot of the Achievements screen
    page.screenshot(path='verification/achievements_screen.png')

    # Try to claim 'slap_master' (y=140 + 85 = 225, x=200)
    page.evaluate('''() => {
        const canvas = document.getElementById('game');
        const rect = canvas.getBoundingClientRect();
        const scaleY = rect.height / canvas.height;
        const scaleX = rect.width / canvas.width;

        const clientX = rect.left + 200 * scaleX;
        const clientY = rect.top + 262 * scaleY; // y=225 + 37.5

        const event = new MouseEvent('click', {
            view: window,
            bubbles: true,
            cancelable: true,
            clientX: clientX,
            clientY: clientY
        });
        canvas.dispatchEvent(event);
    }''')

    page.wait_for_timeout(500)

    # Take screenshot after claiming
    page.screenshot(path='verification/achievements_claimed.png')

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
