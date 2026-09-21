import os
import asyncio
from playwright.async_api import async_playwright

async def run(playwright):
    browser = await playwright.chromium.launch(headless=True)
    page = await browser.new_page()
    await page.goto(f"file://{os.path.abspath('index.html')}")

    # Set canvas size properly
    await page.set_viewport_size({"width": 400, "height": 700})

    # Send Enter key to start the game
    await page.keyboard.press("Enter")

    # Math random logic:
    # We want it to fail: isBomb, isHoming, isSuper, isGolden, isBoomerang, isTrick, isSniper
    # and hit: isGhost
    await page.evaluate("""
        Math.random = function() {
            // isGhost = !isBomb && !isHoming && !isSuper && !isGolden && !isBoomerang && !isTrick && !isSniper && !isFire && Math.random() < 0.15;
            // The checks are:
            // isBomb: 0.08
            // isGolden: 0.05
            // isHoming: 0.10
            // isSuper: 0.18
            // isBoomerang: 0.15
            // isTrick: 0.10
            // isSniper: 0.12
            // We just need a number that is greater than 0.18 but smaller than something else?
            // Actually, each variable is evaluated with a fresh Math.random() call!
            // Wait, the variables are evaluated in order in `spawnChancla`. Let's just return 0.99 for the first 7 calls, then 0.1 for the ghost call.
            if (!window.rngCalls) window.rngCalls = 0;
            window.rngCalls++;
            // 1. isBomb (0.08) -> 0.99
            // 2. isGolden (0.05) -> 0.99
            // 3. isHoming (0.10) -> 0.99
            // 4. isSuper (0.18) -> 0.99
            // 5. isBoomerang (0.15) -> 0.99
            // 6. isTrick (0.10) -> 0.99
            // 7. isSniper (0.12) -> 0.99
            // 8. isFire (0.25) -> 0.99 (or it might be skipped if not enraged)
            // 9. isGhost (0.15) -> 0.10
            // Then it will calculate x, vy, vx, rotSpeed
            // 10. x -> 0.5
            // 11. vy -> 0.5
            // 12. vx -> 0.5
            // 13. rotSpeed -> 0.5

            // To simplify, let's just make Math.random always return 0.14.
            // 0.14 misses isBomb(0.08), misses isGolden(0.05), misses isHoming(0.10), misses isSniper(0.12), misses isTrick(0.10).
            // BUT it hits isBoomerang (0.15)!
            // What if we return 0.2? That misses isBoomerang(0.15), isSuper(0.18).
            // But ghost needs < 0.15.

            // So we NEED a dynamic one.
            if (window.rngCalls % 15 === 8 || window.rngCalls % 15 === 9) {
                return 0.1; // This hits isGhost (and maybe isFire if enraged)
            }
            if (window.rngCalls % 15 < 8) {
                return 0.99; // Bypasses everything else
            }
            return 0.5; // for x, y, vx, vy, etc
        };
    """)

    # Wait for ghost chancla to spawn and be registered
    await page.wait_for_timeout(3000)

    # See what was drawn, should not have crashed
    await page.screenshot(path="screenshot_in_game3.png")

    await browser.close()

async def main():
    async with async_playwright() as playwright:
        await run(playwright)

if __name__ == '__main__':
    asyncio.run(main())
