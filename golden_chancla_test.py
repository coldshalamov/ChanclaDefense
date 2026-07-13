import re

with open("index.html", "r") as f:
    content = f.read()

# 1. spawnChancla
spawn_search = """                const isBomb = Math.random() < 0.08;
                const isHoming = superEnabled && !isBomb && Math.random() < 0.10;
                const isSuper = superEnabled && !isBomb && !isHoming && Math.random() < 0.18;
                const isFire = isa.enraged && !isBomb && !isHoming && !isSuper && Math.random() < 0.25;

                let w = 32;
                let h = 18;
                if (isSuper) { w = 46; h = 26; }
                else if (isBomb) { w = 38; h = 38; }
                else if (isHoming) { w = 36; h = 36; }

                const x = 40 + Math.random() * (canvas.width - 80);
                const y = isa.y + 40;

                let vy = baseSpeed + Math.random() * 60;
                if (isSuper) vy += 40;
                else if (isFire) vy += 80;
                else if (isBomb) vy = baseSpeed * 0.7 + Math.random() * 30; // slower
                else if (isHoming) vy = baseSpeed * 0.8; // slightly slower vertical speed

                const vx = (Math.random() - 0.5) * 60;
                const rotSpeed = (Math.random() - 0.5) * 5;

                let type = 'normal';
                if (isBomb) type = 'bomb';
                else if (isFire) type = 'fire';
                else if (isSuper) type = 'super';
                else if (isHoming) type = 'homing';"""

spawn_replace = """                const isGolden = Math.random() < 0.05;
                const isBomb = !isGolden && Math.random() < 0.08;
                const isHoming = superEnabled && !isGolden && !isBomb && Math.random() < 0.10;
                const isSuper = superEnabled && !isGolden && !isBomb && !isHoming && Math.random() < 0.18;
                const isFire = isa.enraged && !isGolden && !isBomb && !isHoming && !isSuper && Math.random() < 0.25;

                let w = 32;
                let h = 18;
                if (isSuper) { w = 46; h = 26; }
                else if (isBomb) { w = 38; h = 38; }
                else if (isHoming) { w = 36; h = 36; }
                else if (isGolden) { w = 40; h = 40; }

                const x = 40 + Math.random() * (canvas.width - 80);
                const y = isa.y + 40;

                let vy = baseSpeed + Math.random() * 60;
                if (isSuper) vy += 40;
                else if (isFire) vy += 80;
                else if (isGolden) vy += 60;
                else if (isBomb) vy = baseSpeed * 0.7 + Math.random() * 30; // slower
                else if (isHoming) vy = baseSpeed * 0.8; // slightly slower vertical speed

                const vx = (Math.random() - 0.5) * 60;
                const rotSpeed = (Math.random() - 0.5) * 5;

                let type = 'normal';
                if (isGolden) type = 'golden';
                else if (isBomb) type = 'bomb';
                else if (isFire) type = 'fire';
                else if (isSuper) type = 'super';
                else if (isHoming) type = 'homing';"""

content = content.replace(spawn_search, spawn_replace)

# 2. trySlap (the text popups and rewards)
slap_search = """                        // Add float text
                        if (isPerfect) {"""

slap_replace = """                        // Add float text
                        if (c.type === 'golden') {
                            gameData.coins += Math.floor(25 * getPrestigeMultiplier());
                            gameData.stats.totalCoinsEarned += Math.floor(25 * getPrestigeMultiplier());
                            score += Math.floor(500 * getPrestigeMultiplier());
                            addFloatText('GOLDEN SLAP! +25💰✨', c.x, c.y - 10, '#ffd700', 16);
                            spawnImpact(c.x, c.y, true);
                            playSound(850, 0.2);
                            triggerShake(10, 0.3);
                            triggerFlash(0.3, '#ffd700');
                            hitStop = 0.2;
                            spawnRoseExplosion(c.x, c.y);

                            // Reflect all other active chanclas
                            for (let j = 0; j < chanclas.length; j++) {
                                const other = chanclas[j];
                                if (!other.slapped && other !== c && other.type !== 'meteor') {
                                    other.slapped = true;
                                    other.isPerfect = true;
                                    other.vx = (isa.x - other.x) * 2;
                                    other.vy = -600;
                                }
                            }
                        } else if (isPerfect) {"""

content = content.replace(slap_search, slap_replace)

# 3. updateChanclas (boss damage)
damage_search = """                            // Hit Isa
                            let damage = c.type === 'super' ? 15 : (c.type === 'fire' ? 12 : 8);
                            if (c.rallyCount > 0) damage += 10 * c.rallyCount;
                            if (c.type === 'meteor') damage = 40;
                            if (c.type === 'bomb') damage = 20;
                            if (c.isPerfect) damage += 7;"""

damage_replace = """                            // Hit Isa
                            let damage = c.type === 'super' ? 15 : (c.type === 'fire' ? 12 : 8);
                            if (c.rallyCount > 0) damage += 10 * c.rallyCount;
                            if (c.type === 'meteor') damage = 40;
                            if (c.type === 'bomb') damage = 20;
                            if (c.type === 'golden') damage = 35;
                            if (c.isPerfect) damage += 7;"""

content = content.replace(damage_search, damage_replace)

# 4. drawChancla
draw_search = """                // Use the thong sandal emoji for the classic "Chancla" look
                let emoji = '🩴💨';
                if (type === 'super') emoji = '🩴💥';
                else if (type === 'fire') emoji = '🔥';
                else if (type === 'bomb') emoji = '💣';
                else if (type === 'homing') emoji = '🪬';"""

draw_replace = """                // Use the thong sandal emoji for the classic "Chancla" look
                let emoji = '🩴💨';
                if (type === 'super') emoji = '🩴💥';
                else if (type === 'fire') emoji = '🔥';
                else if (type === 'bomb') emoji = '💣';
                else if (type === 'homing') emoji = '🪬';
                else if (type === 'golden') emoji = '✨🥴';"""

content = content.replace(draw_search, draw_replace)

with open("index.html", "w") as f:
    f.write(content)
print("Golden Chancla injected to index.html successfully!")
