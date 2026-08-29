Okay, let's write out the exact plan to implement Trick Chancla (🃏).

1. In `spawnChancla` (in both `index.html` and `chancla_bomb.html`):
Add:
```javascript
const isTrick = !isBomb && !isHoming && !isSuper && !isGolden && !isBoomerang && !isFire && Math.random() < 0.10;
```
Add its dimensions:
```javascript
else if (isTrick) { w = 36; h = 36; }
```
Add it to the type setting block:
```javascript
else if (isTrick) type = 'trick';
```
And modify the `chanclas.push`:
```javascript
chanclas.push({ x, y, vx, vy, vx_saved: vx, vy_saved: vy, w, h, type, rotation: 0, rotSpeed, trickState: 0, trickTimer: 0 });
```

2. In `updateChanclas()` (in both `index.html` and `chancla_bomb.html`):
Right before `// Homing Logic`, add Trick Logic:
```javascript
                    // Trick Logic
                    if (c.type === 'trick' && !c.slapped) {
                        if (c.trickState === 0) {
                            if (c.y > canvas.height * 0.4) {
                                c.trickState = 1;
                                c.trickTimer = 0.5;
                                c.vx_saved = c.vx;
                                c.vy_saved = c.vy;
                                c.vx = 0;
                                c.vy = 0;
                            }
                        } else if (c.trickState === 1) {
                            c.trickTimer -= dt;
                            c.x += (Math.random() - 0.5) * 8; // Vibrate
                            if (c.trickTimer <= 0) {
                                c.trickState = 2;
                                const speed = Math.sqrt(c.vx_saved*c.vx_saved + c.vy_saved*c.vy_saved) * 1.5;
                                const angle = Math.atan2(player.y - c.y, player.x - c.x);
                                c.vx = Math.cos(angle) * speed;
                                c.vy = Math.sin(angle) * speed;
                            }
                        }
                    }
```

Wait, in `trySlap()`:
```javascript
                        if (c.type === 'golden') {
                            // golden stuff
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
                        } else if (isPerfect) {
```

And in `updateChanclas()` boss hit collision:
```javascript
                            let damage = 5;
                            if (c.type === 'super') damage = 15;
                            else if (c.type === 'fire') damage = 10;
                            else if (c.type === 'bomb') damage = 25;
                            else if (c.type === 'golden') damage = 0;
                            else if (c.type === 'trick') damage = 0; // Prevent double dipping
```

And in `drawChancla()`:
```javascript
                else if (type === 'boomerang') emoji = '🪃';
                else if (type === 'trick') emoji = '🃏';
```
```javascript
                    } else if (type === 'golden') {
                        ctx.shadowColor = '#ffd700';
                        ctx.shadowBlur = 20;
                    } else if (type === 'trick') {
                        ctx.shadowColor = '#ff00ff';
                        ctx.shadowBlur = 15;
                    }
```

This perfectly matches memory instructions for Trick Chancla.
