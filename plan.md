1. *Modify gameData initialization*
   - Add `wins: 1` to the default `gameData.stats` object.
   - Add a fallback check `if (!gameData.stats.wins) gameData.stats.wins = 1;` in the load block.
2. *Create `triggerWin()` function*
   - Replace the inline `isa.anger <= 0` win logic with a new `triggerWin()` function.
   - This function will increment `gameData.stats.wins`, calculate the coin bonus `50 + (defeatedLevel - 1) * 50`, add it to the player's total, and save the data.
3. *Implement difficulty scaling in `resetGame()`*
   - Update `isa.maxAnger = 100 + (wins - 1) * 20` and `isa.anger = isa.maxAnger`.
   - Update `spawnInterval = Math.max(0.2, 1.2 - (wins - 1) * 0.05)`.
   - Update `minSpawnInterval = Math.max(0.1, 0.45 - (wins - 1) * 0.02)`.
   - Update `baseSpeed = 140 + (wins - 1) * 5`.
4. *Update UI to show levels*
   - Title screen: Add Level indication to the subtitle.
   - Win screen: Show the defeated level and the scaling bonus coins rewarded.
5. *Apply to both HTML files*
   - Make sure identical changes are applied to `index.html` and `chancla_bomb.html`.
6. *Ensure proper testing, verification, review, and reflection are done*
   - I will call the pre_commit_instructions tool to complete the necessary pre-commit steps.
7. *Submit the changes.*
   - Submit the changes using the git commit branch.
