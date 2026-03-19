import asyncio
from playwright.async_api import async_playwright
import os

async def verify():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={'width': 450, 'height': 800},
            has_touch=True,
            is_mobile=True,
            device_scale_factor=1,
        )
        page = await context.new_page()

        # Give enough coins and stats to claim the first achievement
        await page.add_init_script("""
            localStorage.setItem('chancla_bomb_save', JSON.stringify({
                coins: 5,
                upgrades: { lives: 0, shield: 0, cooldown: 0, speed: 0 },
                bestScore: 10,
                stats: { totalSlaps: 1, perfectSlaps: 0, gamesPlayed: 0, totalCoinsEarned: 0 },
                achievements: {}
            }));
        """)

        await page.goto('file://' + os.getcwd() + '/index.html')
        await page.wait_for_timeout(500)

        # Click Achiev button
        await page.evaluate("""
            const evt = new MouseEvent('click', {
                clientX: 225,
                clientY: 570,
                bubbles: true
            });
            document.querySelector('canvas').dispatchEvent(evt);
        """)
        await page.wait_for_timeout(500)
        await page.screenshot(path='verification/achievements_menu.png')

        await browser.close()

asyncio.run(verify())
