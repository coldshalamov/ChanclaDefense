1. **Implement Trick Chancla in `spawnChancla()` (in both `index.html` and `chancla_bomb.html`)**
   - Add `const isTrick = !isBomb && !isHoming && !isSuper && !isGolden && !isBoomerang && !isFire && Math.random() < 0.10;` after the boolean logic for others.
   - Set width/height: `else if (isTrick) { w = 36; h = 36; }`
   - Set type: `else if (isTrick) type = 'trick';`
   - Modify the push statement to initialize saved velocities and trick state: `chanclas.push({ x, y, vx, vy, vx_saved: vx, vy_saved: vy, w, h, type, rotation: 0, rotSpeed, trickState: 0, trickTimer: 0 });`
   - (Run `grep` / `cat` locally to ensure exact replacement locations).

2. **Add behavior to `updateChanclas()` (in both `index.html` and `chancla_bomb.html`)**
   - Above the existing `// Homing Logic`, insert the state machine for `trick` type.
   - It will check `c.trickState === 0` to see if `c.y > canvas.height * 0.4` (Wait, memory says "pauses mid-air", I will use `canvas.height * 0.4`), transition to `trickState = 1`, save velocities to `vx_saved` and `vy_saved` and set them to 0.
   - In `trickState === 1`, it vibrates and counts down `trickTimer`.
   - Once `trickTimer <= 0`, it goes to `trickState = 2`, calculates a darting trajectory straight at `player` using `speed = Math.sqrt(c.vx_saved*c.vx_saved + c.vy_saved*c.vy_saved) * 1.5;`.
   - Also, in the boss hit logic within `updateChanclas()`, set `damage = 0` if `c.type === 'trick'` to prevent double-dipping.

3. **Add scoring and damage to `trySlap()` (in both `index.html` and `chancla_bomb.html`)**
   - Before `else if (isPerfect) {`, add `else if (c.type === 'trick') {` to handle the specific Trick Chancla slap rewards (15 base pts, 10 damage to boss, trigger flash/impact/sound, and display "TRICKED! 🃏").

4. **Update `drawChancla()` to render Trick Chancla (in both `index.html` and `chancla_bomb.html`)**
   - Assign emoji: `else if (type === 'trick') emoji = '🃏';`
   - Add glowing shadow: `else if (type === 'trick') { ctx.shadowColor = '#ff00ff'; ctx.shadowBlur = 15; }`

5. **Verify implementation**
   - Use `grep -A` to verify modifications were made properly to `index.html` and `chancla_bomb.html`.
   - Run python verification tests to check functionality (`python3 verification/test_game.py` or similar).

6. Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.
