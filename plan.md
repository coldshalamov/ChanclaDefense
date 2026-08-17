1. **Apply the boomerang chancla feature to `index.html` via a python script:**
   - Modify `spawnChancla` to randomly determine if it's a boomerang (`const isBoomerang = !isBomb && !isHoming && !isSuper && Math.random() < 0.15;`).
   - Add logic for width/height and emoji (🪃) assignment for the new `boomerang` type.
   - Modify `updateChanclas` so that if a boomerang chancla reaches the bottom (`c.y > canvas.height + c.h`) and hasn't yet returned (`!c.returning`), it reverses velocity (`c.vy = -c.vy`), sets `c.returning = true`, updates its Y coordinate, and displays "SWOOP! 🪃". Otherwise, it splices normally.
   - The exact script content will be:
```python
import re

with open('index.html', 'r') as f:
    content = f.read()

replace1 = """                const isBomb = Math.random() < 0.08;
                const isHoming = superEnabled && !isBomb && Math.random() < 0.10;
                const isSuper = superEnabled && !isBomb && !isHoming && Math.random() < 0.18;
                const isBoomerang = !isBomb && !isHoming && !isSuper && Math.random() < 0.15;
                const isFire = isa.enraged && !isBomb && !isHoming && !isSuper && !isBoomerang && Math.random() < 0.25;

                let w = 32;
                let h = 18;
                if (isSuper) { w = 46; h = 26; }
                else if (isBomb) { w = 38; h = 38; }
                else if (isHoming) { w = 36; h = 36; }
                else if (isBoomerang) { w = 34; h = 20; }"""

replace2 = """                else if (isBomb) vy = baseSpeed * 0.7 + Math.random() * 30; // slower
                else if (isHoming) vy = baseSpeed * 0.8; // slightly slower vertical speed
                else if (isBoomerang) vy = baseSpeed * 1.1;

                const vx = (Math.random() - 0.5) * 60;
                const rotSpeed = (Math.random() - 0.5) * 5;

                let type = 'normal';
                if (isBomb) type = 'bomb';
                else if (isFire) type = 'fire';
                else if (isSuper) type = 'super';
                else if (isHoming) type = 'homing';
                else if (isBoomerang) type = 'boomerang';

                chanclas.push({ x, y, vx, vy, w, h, type, rotation: 0, rotSpeed });"""

replace3 = """                // Use the thong sandal emoji for the classic "Chancla" look
                let emoji = '🩴💨';
                if (type === 'super') emoji = '🩴💥';
                else if (type === 'fire') emoji = '🔥';
                else if (type === 'bomb') emoji = '💣';
                else if (type === 'homing') emoji = '🪬';
                else if (type === 'boomerang') emoji = '🪃';"""

replace4 = """                        } else {
                            score += Math.floor(1 * getPrestigeMultiplier());
                            const prevBest = bestScore;
                            bestScore = Math.max(bestScore, score);
                            if (score > prevBest && score % 10 === 0) sayRandom('highScore');
                            if (Math.random() < 0.2) sayRandom('nearMiss');
                            if (Math.random() < 0.25) sayPlayer('nearMiss');
                        }

                        if (c.type === 'boomerang' && !c.returning) {
                            c.returning = true;
                            c.vy = -c.vy;
                            c.y = canvas.height + c.h;
                            addFloatText('SWOOP! 🪃', c.x, canvas.height - 20);
                        } else {
                            chanclas.splice(i, 1);
                        }
                    }
                }
            }"""

content1 = content.replace("""                const isBomb = Math.random() < 0.08;
                const isHoming = superEnabled && !isBomb && Math.random() < 0.10;
                const isSuper = superEnabled && !isBomb && !isHoming && Math.random() < 0.18;
                const isFire = isa.enraged && !isBomb && !isHoming && !isSuper && Math.random() < 0.25;

                let w = 32;
                let h = 18;
                if (isSuper) { w = 46; h = 26; }
                else if (isBomb) { w = 38; h = 38; }
                else if (isHoming) { w = 36; h = 36; }""", replace1)

content2 = content1.replace("""                else if (isBomb) vy = baseSpeed * 0.7 + Math.random() * 30; // slower
                else if (isHoming) vy = baseSpeed * 0.8; // slightly slower vertical speed

                const vx = (Math.random() - 0.5) * 60;
                const rotSpeed = (Math.random() - 0.5) * 5;

                let type = 'normal';
                if (isBomb) type = 'bomb';
                else if (isFire) type = 'fire';
                else if (isSuper) type = 'super';
                else if (isHoming) type = 'homing';

                chanclas.push({ x, y, vx, vy, w, h, type, rotation: 0, rotSpeed });""", replace2)

content3 = content2.replace("""                // Use the thong sandal emoji for the classic "Chancla" look
                let emoji = '🩴💨';
                if (type === 'super') emoji = '🩴💥';
                else if (type === 'fire') emoji = '🔥';
                else if (type === 'bomb') emoji = '💣';
                else if (type === 'homing') emoji = '🪬';""", replace3)

content4 = content3.replace("""                        } else {
                            score += Math.floor(1 * getPrestigeMultiplier());
                            const prevBest = bestScore;
                            bestScore = Math.max(bestScore, score);
                            if (score > prevBest && score % 10 === 0) sayRandom('highScore');
                            if (Math.random() < 0.2) sayRandom('nearMiss');
                            if (Math.random() < 0.25) sayPlayer('nearMiss');
                        }
                        chanclas.splice(i, 1);
                    }
                }
            }""", replace4)

with open('index.html', 'w') as f:
    f.write(content4)
```

2. **Apply the exact same changes to `chancla_bomb.html`.** We will use the same string replacement approach via a Python script.

3. **Verify the applied edits using `grep`** to ensure `boomerang` related changes are successfully injected in both files.

4. **Run `python3 verification/test_game.py`** to quickly ensure the game loads without syntax errors.

5. Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.
