1. **Understand the Goal**: The user wants to improve the game "Chancla Bomb: Isa vs. Su Gringo Para Siempre" to make it more interesting for modern players. The game is an endless runner / tapping game where the player has to slap away incoming "chanclas" (sandals).
2. **Identify Weaknesses**:
   - The game loop is very repetitive.
   - The player only moves left and right and slaps.
   - There is no sense of progression within a single run, other than the speed getting faster and more chanclas spawning.
   - There's no way to actively avoid damage other than moving or slapping.
3. **Propose an Improvement**: Add a **Dash Mechanic**. This is a staple in modern action/arcade games. It gives the player a tool to reposition quickly and gain temporary invincibility, adding depth to the movement.
   - **Details**:
     - The dash can be triggered by pressing the 'Shift' key (desktop) or double-tapping a movement direction (mobile).
     - During the dash, the player moves much faster for a short duration.
     - The player is invincible during the dash (`player.dashTimer > 0`).
     - There is a cooldown for the dash to prevent spamming (`player.dashCooldown > 0`).
     - Visual feedback: A trail behind the player when dashing.
4. **Implementation Steps**:
   - Add dash state variables to the `player` object: `dashTimer`, `dashCooldown`, `dashDir`.
   - Add a `dashTrails` array to keep track of trail visual effects.
   - Update `resetGame` to initialize these variables.
   - Update `handleKey` to trigger dash on 'Shift'.
   - Update touch event listeners to trigger dash on double tap (need to track `lastTapLeft` and `lastTapRight`).
   - Update the `update` loop to handle dash movement, timers, and trail spawning.
   - Update `updateChanclas` to check for invincibility if `player.dashTimer > 0`.
   - Update the `draw` loop to render dash trails.
   - Ensure these changes are applied to **both** `index.html` and `chancla_bomb.html` as they share logic.
