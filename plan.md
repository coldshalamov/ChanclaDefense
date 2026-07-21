1. **Add "Golden Chancla" logic to `spawnChancla` in `index.html` and `chancla_bomb.html`**
   - Modify probabilities to include `isGolden = Math.random() < 0.05`. Ensure it takes precedence or is mutually exclusive with others.
   - Set `type = 'golden'`.
2. **Add visual emoji in `drawChancla`**
   - In `drawChancla`, set `emoji = '✨🥺'` if `type === 'golden'`.
   - Add shadow effect `ctx.shadowColor = 'gold'` for `type === 'golden'`.
3. **Handle mechanics in `trySlap`**
   - When successfully slapped, if `type === 'golden'`:
     - `score += Math.floor(500 * getPrestigeMultiplier());`
     - `gameData.coins += Math.floor(25 * getPrestigeMultiplier());`
     - `gameData.stats.totalCoinsEarned += Math.floor(25 * getPrestigeMultiplier());`
     - `triggerFlash(0.3, '#ffd700');`
     - Iterate through all `chanclas`, and if `!other.slapped`, set `slapped = true`, `vy = -600`, `vx = (isa.x - other.x) * 1.5`, `rotSpeed = 25`.
4. **Handle damage when hitting Isa**
   - In the update loop where slapped chanclas hit `isa`, add `if (c.type === 'golden') damage = 35;`.
5. **Verify Changes**
   - Run a python script using Playwright to test if Golden Chancla spawns and its effects apply correctly.
6. **Pre-commit Steps**
   - Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.
