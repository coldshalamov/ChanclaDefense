plan = """
I will implement an upgrade for the game to improve replayability and persistence.

Based on the game memory and codebase, I will implement a "Slap Power" upgrade.

Steps:
1. Update `gameData` initialization in both `index.html` and `chancla_bomb.html` to include `power: 0` in `gameData.upgrades`.
2. Add `power` to the upgrade shop list in `index.html` and `chancla_bomb.html` in the three locations where `const upgrades = [...]` is defined:
   - In the shop rendering logic (`state === STATE.SHOP` drawing phase).
   - In the touch event listener `handleInput` (click/touch) for shop upgrade buttons (`state === STATE.SHOP`).
   - In the fallback mouse event listener.
3. Modify the damage logic to incorporate `gameData.upgrades.power`:
   - Calculate `powerLevel = gameData.upgrades.power || 0;`
   - In the normal reflection hit logic (`damage` calculation):
     - Normal reflected chanclas deal an additional `powerLevel * 2` damage.
   - In the special attack hit logic:
     - The special attack deals `20 + (powerLevel * 5)` damage instead of a flat 20.
4. Run pre-commit checks and verify everything works.
5. Commit the changes and submit.
"""
print(plan)
