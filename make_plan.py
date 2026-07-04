plan = """
1. **Add `PRESTIGE` to `STATE` definition** in both HTML files:
   - Modify `const STATE = { TITLE: 'title', PLAYING: 'playing', GAMEOVER: 'gameover', WIN: 'win', SHOP: 'shop', ACHIEVEMENTS: 'achievements', COSMETICS: 'cosmetics' };`
   - To include `PRESTIGE: 'prestige'`.

2. **Initialize `gameData.prestige`** in both HTML files:
   - Add `if (!gameData.prestige) gameData.prestige = 0;` near the `gameData` property checks.

3. **Render Prestige Button on Title Screen** in both HTML files:
   - Inside `function drawTitleScreen()`, add a check `if (gameData.stats.wins >= 10) { ... }`.
   - Render the button using `roundRect(ctx, 110, 620, canvas.width - 220, 46, 12);` with color e.g., `#f44336` and text "Prestige / Prestigio".

4. **Add Prestige Button Click Handlers on Title Screen** in both HTML files:
   - In both `canvas.addEventListener('click', ...)` and `canvas.addEventListener('touchstart', ...)`.
   - Add logic for hitting the button at `y >= 620 && y <= 666` and transitioning to `state = STATE.PRESTIGE;`.

5. **Create `function drawPrestige()`** in both HTML files:
   - Render background, title, description, benefits (e.g. `1 + gameData.prestige * 0.5` multiplier), and a big CONFIRM button, plus a BACK button.

6. **Add Click/Touch Handlers for `STATE.PRESTIGE`** in both HTML files:
   - In click and touch listeners, handle `state === STATE.PRESTIGE`.
   - Click "Confirm": Increment `gameData.prestige++`, reset `wins = 1`, `coins = 0`, `upgrades = { lives: 0, shield: 0, cooldown: 0, speed: 0, power: 0 }`, save data, and go back to `STATE.TITLE`.
   - Click "Back": Go back to `STATE.TITLE`.

7. **Apply Prestige Multiplier** in both HTML files:
   - Update score gains in `trySlap`, `triggerGraze`, `update(dt)` (fiesta score), and `endGame()`.
   - The multiplier should be `const mult = (1 + (gameData.prestige || 0) * 0.5);`.
   - Apply this multiplier to `gameData.coins += 2`, `gameData.coins += 1`, `gameData.coins += bonus`, `gameData.coins += earned` (maybe not achievement rewards to keep it fair, or apply there too, memory says "most coin and score calculations"). I will apply it to score and coins earned through gameplay (slaps, boss kill, end game bonus).
"""
print(plan)
