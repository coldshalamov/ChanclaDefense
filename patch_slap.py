def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    old_slap = """                        // Add float text
                        if (isPerfect) {
                            gameData.coins += 2;
                            addFloatText('PERFECT! +2💰' + comboText, c.x, c.y - 10);
                            spawnImpact(c.x, c.y, true);
                            playSound(850, 0.15);
                            triggerShake(6, 0.2);
                            triggerFlash(0.15, '#fff');
                            hitStop = 0.15;
                            spawnRoseExplosion(c.x, c.y);
                        } else {
                            gameData.coins += 1;
                            addFloatText('SLAP! +1💰' + comboText, c.x, c.y);
                            spawnImpact(c.x, c.y);
                            playSound(600, 0.1);
                        }"""

    new_slap = """                        // Add float text
                        if (c.type === 'golden') {
                            gameData.coins += 15;
                            score += 50;
                            specialAttackBar = Math.min(maxSpecialAttack, specialAttackBar + 50);
                            addFloatText('GOLDEN! +15💰' + comboText, c.x, c.y - 15);
                            spawnImpact(c.x, c.y, true);
                            playSound(1200, 0.2);
                            triggerShake(8, 0.25);
                            triggerFlash(0.2, '#ffd700'); // gold flash
                            hitStop = 0.2;
                            spawnRoseExplosion(c.x, c.y);
                        } else if (isPerfect) {
                            gameData.coins += 2;
                            addFloatText('PERFECT! +2💰' + comboText, c.x, c.y - 10);
                            spawnImpact(c.x, c.y, true);
                            playSound(850, 0.15);
                            triggerShake(6, 0.2);
                            triggerFlash(0.15, '#fff');
                            hitStop = 0.15;
                            spawnRoseExplosion(c.x, c.y);
                        } else {
                            gameData.coins += 1;
                            addFloatText('SLAP! +1💰' + comboText, c.x, c.y);
                            spawnImpact(c.x, c.y);
                            playSound(600, 0.1);
                        }"""

    content = content.replace(old_slap, new_slap, 1)

    with open(filepath, 'w') as f:
        f.write(content)

patch_file('index.html')
patch_file('chancla_bomb.html')
