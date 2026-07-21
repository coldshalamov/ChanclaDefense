1. **Explore the codebase**:
   - Analyzed the current mechanics and chancla types (normal, super, fire, bomb, homing, meteor).
2. **Brainstorm 10 fun and interesting ideas**:
   1. *Trick Chancla (🃏)*: Pauses mid-air and darts at the player.
   2. *Golden Chancla (✨🥺)*: Rare, highly rewarding, and reflects all other active chanclas.
   3. *Ghost Chancla (👻)*: Turns invisible halfway down.
   4. *Mirror Mode*: Swaps left/right controls randomly.
   5. *Bouncy Chancla (🏀)*: Bounces off screen edges.
   6. *Giant Chancla (🩴🦵)*: Huge, slow, takes multiple slaps.
   7. *Time Freeze Chancla (⏱️)*: Slapping it freezes time for a few seconds.
   8. *Magnet Chancla (🧲)*: Sucks the player towards it.
   9. *Clone Chancla (👯)*: Splits into two if not perfectly slapped.
   10. *Black Hole Chancla (🌌)*: Sucks in other chanclas while falling.
3. **Select the best idea and implement it**:
   - I select the **Golden Chancla (✨🥺)** because it synergizes beautifully with the existing mechanics, rewards the player in multiple dimensions (huge points, coins, boss damage), and creates an awesome chain-reaction moment (reflecting all other chanclas).
4. **Implement Golden Chancla in `index.html` and `chancla_bomb.html`**:
   - **Verification**: Check if `spawnChancla`, `drawChancla`, `trySlap`, and the `Hit Isa` logic exist via `grep`. (Completed previously, all exist and logic is clear).
   - Update `spawnChancla` to spawn it with a 5% chance.
   - Update `drawChancla` to render `✨🥺` with a golden glow (`#ffd700`).
   - Update `trySlap` to award 500 bonus points, 25 coins, trigger a golden flash (`triggerFlash(0.3, '#ffd700')`), and loop over other active chanclas, setting them to `slapped = true`, `vx = (isa.x - other.x) * 1.5`, and `vy = -600`.
   - Update the Isa damage calculation to deal 35 base damage when `c.type === 'golden'`.
5. **Run the test suite**:
   - Run `python3 -m pytest verification/` to ensure no regressions occur.
6. Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.
7. **Submit the changes**.
