import re

plan = """
I am implementing the Prestige System as mentioned in the memory constraints.
The memory explicitly states:
- Game has a "Prestige" system (`STATE.PRESTIGE`).
- Needs `gameData.stats.wins >= 10` to trigger.
- Prestiging resets wins, coins, upgrades.
- Increments `gameData.prestige`.
- Grants a permanent `0.5x` multiplier (`1 + gameData.prestige * 0.5`) to score and coin calculations.
- Rendered on Title Screen at `y = 620` conditionally.

Plan Details:
1. Update `const STATE` and add `PRESTIGE: 'prestige'` in both `index.html` and `chancla_bomb.html`.
2. Update `gameData` initialization to include `prestige: 0`.
3. In `drawTitleScreen()`, render the Prestige button if `gameData.stats.wins >= 10`.
4. In `drawPrestige()`, render the Prestige screen with "Confirm" and "Back" buttons.
5. In the click/touchstart handlers for `STATE.TITLE`, add logic to handle the button at `y=620`.
6. Add click/touchstart handlers for `STATE.PRESTIGE` to handle "Confirm" (perform reset, increment `gameData.prestige`, go to `TITLE`) and "Back" (go to `TITLE`).
7. Update `score` and `coins` variables using the multiplier `(1 + (gameData.prestige || 0) * 0.5)`. I will apply this to `trySlap`, `endGame`, `triggerWin`, and passive/graze scores.
8. Add `drawPrestige()` to the main render `loop`.
9. Ensure tests pass and run `pytest verification/`.
10. Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.
"""

with open('plan.md', 'w') as f:
    f.write(plan)
