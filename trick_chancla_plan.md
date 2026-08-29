Based on memory and code inspection, let's implement the **Trick Chancla** (🃏).
This is in memory as something that should be implemented.
- The 'Trick Chancla' (emoji: 🃏, purple glow: ctx.shadowColor = '#ff00ff') is a projectile type (10% spawn chance) that pauses mid-air, vibrates, and darts rapidly at the player.
- Successfully slapping it awards 15 base bonus points, deals 10 damage to the boss, and displays 'TRICKED! 🃏'.
- Memory guidelines for darting speed: "Calculate the projectile's current speed using its saved velocity components instead: `Math.sqrt(c.vx_saved*c.vx_saved + c.vy_saved*c.vy_saved)`." (Wait, we should save `vx` and `vy` in `trickState` or as `vx_saved`, `vy_saved` in the object).
- Memory says: "Chancla projectile objects contain properties: x, y, vx, vy, vx_saved, vy_saved, w, h, type ..., trickState, and trickTimer."

Let's modify `index.html` and `chancla_bomb.html`:
1. In `spawnChancla()`: Add 10% spawn chance for trick. `const isTrick = !isBomb && !isHoming && !isSuper && !isGolden && !isBoomerang && !isFire && Math.random() < 0.10;`
Wait, order of checks matters. Memory says: 10% spawn chance.
Let's see: `isGolden` is 5%. Then `isHoming` is 10%. Then `isSuper` 18%. `isBoomerang` 15%. `isFire` 25%. `isTrick` can be placed anywhere, maybe after `isGolden`. Let's just put it in the else chain.
`const isTrick = !isBomb && !isHoming && !isSuper && !isGolden && !isBoomerang && !isFire && Math.random() < 0.10;` (Wait, if they are mutually exclusive, any order works. Let's make sure probabilities add up logically).
Let's look at how spawnChancla defines them:
```javascript
const isBomb = Math.random() < 0.08;
const isGolden = !isBomb && Math.random() < 0.05;
const isTrick = !isBomb && !isGolden && Math.random() < 0.10;
```
Wait, if `isTrick` goes after `isGolden`, it shifts the others. I will just add it.
Then set `c.vx_saved = c.vx; c.vy_saved = c.vy; c.trickState = 0; c.trickTimer = 0;` for trick.

2. In `updateChanclas()`:
```javascript
// Trick logic
if (c.type === 'trick' && !c.slapped) {
    if (c.trickState === 0) {
        if (c.y > canvas.height * 0.3) {
            c.trickState = 1; // Pause
            c.trickTimer = 0.6; // pause for 0.6s
            c.vx_saved = c.vx;
            c.vy_saved = c.vy;
            c.vx = 0;
            c.vy = 0;
        }
    } else if (c.trickState === 1) {
        c.trickTimer -= dt;
        c.x += (Math.random() - 0.5) * 10; // vibrate
        if (c.trickTimer <= 0) {
            c.trickState = 2; // Dart
            const speed = Math.sqrt(c.vx_saved*c.vx_saved + c.vy_saved*c.vy_saved) * 1.5; // faster dart
            const angle = Math.atan2(player.y - c.y, player.x - c.x);
            c.vx = Math.cos(angle) * speed;
            c.vy = Math.sin(angle) * speed;
        }
    }
}
```

3. In `drawChancla()`:
```javascript
else if (type === 'trick') emoji = '🃏';
...
else if (type === 'trick') {
    ctx.shadowColor = '#ff00ff';
    ctx.shadowBlur = 15;
}
```

4. In `trySlap()`:
```javascript
if (c.type === 'golden') {
   ...
} else if (c.type === 'trick') {
    gameData.coins += Math.floor(2 * getPrestigeMultiplier());
    gameData.stats.totalCoinsEarned += Math.floor(2 * getPrestigeMultiplier());
    score += Math.floor(15 * getPrestigeMultiplier());
    triggerFlash(0.2, '#ff00ff');
    addFloatText('TRICKED! 🃏', c.x, c.y, '#ff00ff');
    isa.anger = Math.max(0, isa.anger - 10);
    if (isa.anger <= 0) triggerWin();
    spawnImpact(c.x, c.y, true);
    playSound(850, 0.2);
}
```

Wait, memory says: "When a special projectile (like the Golden Chancla or Trick Chancla) directly applies damage to the boss within the trySlap() function, ensure its standard collision damage in updateChanclas() is explicitly set to 0 (e.g., if (c.type === 'golden') damage = 0;) to prevent double-dipping boss damage."

Let's check `trySlap()` to see if `isa.anger` is modified. And wait, standard collision damage? That means when slapped, it flies up, hits the boss, and in `updateChanclas()` it checks `if (c.slapped && c.y < isa.y + 100 ...) isa.anger -= damage`.
Let's verify this collision logic in `updateChanclas()`.
