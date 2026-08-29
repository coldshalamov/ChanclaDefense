1. **Implement Trick Chancla in `spawnChancla()` (in both `index.html` and `chancla_bomb.html`)**
   - Execute python script to explicitly target the boolean checks, the type assignments, the dimensions, and the push.
```python
import os

files = ['index.html', 'chancla_bomb.html']
for filepath in files:
    with open(filepath, 'r') as f:
        content = f.read()

    # Booleans
    content = content.replace(
        "const isBoomerang = !isBomb && !isHoming && !isSuper && !isGolden && Math.random() < 0.15;",
        "const isBoomerang = !isBomb && !isHoming && !isSuper && !isGolden && Math.random() < 0.15;\n                const isTrick = !isBomb && !isHoming && !isSuper && !isGolden && !isBoomerang && !isFire && Math.random() < 0.10;"
    )

    # Dimensions
    content = content.replace(
        "else if (isGolden) { w = 36; h = 20; }",
        "else if (isGolden) { w = 36; h = 20; }\n                else if (isTrick) { w = 36; h = 36; }"
    )

    # Type
    content = content.replace(
        "else if (isGolden) type = 'golden';",
        "else if (isGolden) type = 'golden';\n                else if (isTrick) type = 'trick';"
    )

    # push statement
    content = content.replace(
        "chanclas.push({ x, y, vx, vy, w, h, type, rotation: 0, rotSpeed });",
        "chanclas.push({ x, y, vx, vy, vx_saved: vx, vy_saved: vy, w, h, type, rotation: 0, rotSpeed, trickState: 0, trickTimer: 0, dodged: false, returning: false, invisible: false });"
    )

    with open(filepath, 'w') as f:
        f.write(content)
```

2. **Add behavior to `updateChanclas()` (in both `index.html` and `chancla_bomb.html`)**
   - Execute script to inject Trick Logic before Homing Logic, and to prevent double-dipping boss damage.
```python
trick_logic = """                    // Trick Logic
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

                    // Homing Logic"""

import os
files = ['index.html', 'chancla_bomb.html']
for filepath in files:
    with open(filepath, 'r') as f:
        content = f.read()

    content = content.replace("// Homing Logic", trick_logic)
    content = content.replace("if (c.type === 'golden') damage = 0; // Prevent double-dipping as damage is applied in trySlap", "if (c.type === 'golden') damage = 0; // Prevent double-dipping as damage is applied in trySlap\n                            if (c.type === 'trick') damage = 0; // Prevent double dipping")

    with open(filepath, 'w') as f:
        f.write(content)
```

3. **Add scoring and damage to `trySlap()` (in both `index.html` and `chancla_bomb.html`)**
   - Execute python script.
```python
trick_slap = """                        } else if (c.type === 'trick') {
                            gameData.coins += Math.floor(2 * getPrestigeMultiplier());
                            gameData.stats.totalCoinsEarned += Math.floor(2 * getPrestigeMultiplier());
                            score += Math.floor(15 * getPrestigeMultiplier());
                            triggerFlash(0.2, '#ff00ff');
                            addFloatText('TRICKED! 🃏', c.x, c.y, '#ff00ff');
                            isa.anger = Math.max(0, isa.anger - 10);
                            if (isa.anger <= 0) triggerWin();
                            spawnImpact(c.x, c.y, true);
                            playSound(850, 0.2);
                        } else if (isPerfect) {"""

import os
files = ['index.html', 'chancla_bomb.html']
for filepath in files:
    with open(filepath, 'r') as f:
        content = f.read()

    content = content.replace("} else if (isPerfect) {", trick_slap)
    with open(filepath, 'w') as f:
        f.write(content)
```

4. **Update `drawChancla()` to render Trick Chancla (in both `index.html` and `chancla_bomb.html`)**
   - Execute python script.
```python
import os
files = ['index.html', 'chancla_bomb.html']
for filepath in files:
    with open(filepath, 'r') as f:
        content = f.read()

    content = content.replace("else if (type === 'golden') emoji = '✨👞';", "else if (type === 'golden') emoji = '✨👞';\n                else if (type === 'trick') emoji = '🃏';")

    shadow_replace = """                    } else if (type === 'homing') {
                        ctx.shadowColor = '#8a2be2';
                        ctx.shadowBlur = 15;
                    } else if (type === 'trick') {
                        ctx.shadowColor = '#ff00ff';
                        ctx.shadowBlur = 15;
                    } else if (type === 'golden') {"""

    original_shadow = """                    } else if (type === 'homing') {
                        ctx.shadowColor = '#8a2be2';
                        ctx.shadowBlur = 15;
                    } else if (type === 'golden') {"""

    content = content.replace(original_shadow, shadow_replace)

    with open(filepath, 'w') as f:
        f.write(content)
```

5. **Verify file modifications**
   - Use `grep -C 5 "c.trickState"` index.html and chancla_bomb.html to verify updates were applied correctly.
   - Use `grep -C 5 "TRICKED"` index.html and chancla_bomb.html to verify updates were applied correctly.
   - Use `grep -C 5 "emoji = '🃏'"` index.html and chancla_bomb.html to verify updates were applied correctly.

6. **Verify implementation**
   - Run `python3 verification/test_game.py` to check functionality.

7. Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.
