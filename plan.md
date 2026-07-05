1. **Analyze the problem**: Implement a Prestige system to add persistent replay value to the game. When a player clears Boss Level 10, they can Prestige. Prestiging resets their coins, level (wins), and upgrades, but increases their `prestige` count. Each prestige level grants a permanent +50% multiplier to coins and score from core gameplay loops.

2. **File Modifications**: Apply identical changes to `index.html` and `chancla_bomb.html`.
   - Update `STATE`: Add `PRESTIGE: 'prestige'`
   - Update `gameData` definition to include `prestige: 0`.
   - Add legacy save migration: `if (typeof gameData.prestige === 'undefined') gameData.prestige = 0;`
   - Update `drawTitleScreen` to display the current prestige level (if > 0) next to the Level text.
   - Add a "Prestige" button on the Title Screen at `y=620`.
   - Implement `drawPrestige()` function to render the Prestige screen showing requirements, benefits, and action buttons.
   - Update click and touch event listeners to handle transitions to/from `STATE.PRESTIGE` and the prestige action.
   - Update core gameplay loops (`update`, `trySlap`, `endGame`, `triggerWin`) to apply the prestige multiplier `const mult = 1 + (gameData.prestige || 0) * 0.5;` to `score` and `coins` increments (using `Math.ceil` for coins).

3. **Write a Python patch script**:
   - Instead of manual string manipulation, write a robust Python script to handle the injections for both HTML files using `replace` or `re.sub`.
   - Add verification to check if the changes were applied correctly using `grep`.
   - Run the test suite.

4. **Complete Pre-commit and Submit**.
