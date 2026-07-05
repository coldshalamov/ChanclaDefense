import re

def update_file(filename):
    with open(filename, 'r') as f:
        content = f.read()

    # 1. Update spawnChancla
    spawn_search = """                const isSuper = superEnabled && !isBomb && !isHoming && Math.random() < 0.18;
                const isFire = isa.enraged && !isBomb && !isHoming && !isSuper && Math.random() < 0.25;"""
    spawn_replace = """                const isSuper = superEnabled && !isBomb && !isHoming && Math.random() < 0.18;
                const isFire = isa.enraged && !isBomb && !isHoming && !isSuper && Math.random() < 0.25;
                const isGolden = !isBomb && !isHoming && !isSuper && !isFire && Math.random() < 0.02;"""
    content = content.replace(spawn_search, spawn_replace)

    spawn_w_search = """                else if (isHoming) { w = 36; h = 36; }"""
    spawn_w_replace = """                else if (isHoming) { w = 36; h = 36; }
                else if (isGolden) { w = 40; h = 22; }"""
    content = content.replace(spawn_w_search, spawn_w_replace)

    spawn_vy_search = """                else if (isHoming) vy = baseSpeed * 0.8; // slightly slower vertical speed"""
    spawn_vy_replace = """                else if (isHoming) vy = baseSpeed * 0.8; // slightly slower vertical speed
                else if (isGolden) vy = baseSpeed * 1.5 + 50; // much faster"""
    content = content.replace(spawn_vy_search, spawn_vy_replace)

    spawn_type_search = """                else if (isHoming) type = 'homing';"""
    spawn_type_replace = """                else if (isHoming) type = 'homing';
                else if (isGolden) type = 'golden';"""
    content = content.replace(spawn_type_search, spawn_type_replace)

    # 2. Update drawChancla
    draw_search = """                else if (type === 'homing') emoji = '🪬';"""
    draw_replace = """                else if (type === 'homing') emoji = '🪬';
                else if (type === 'golden') emoji = '🩴✨';"""
    content = content.replace(draw_search, draw_replace)

    draw_shadow_search = """                    } else if (type === 'homing') {
                        ctx.shadowColor = '#8a2be2';
                        ctx.shadowBlur = 15;
                    }"""
    draw_shadow_replace = """                    } else if (type === 'homing') {
                        ctx.shadowColor = '#8a2be2';
                        ctx.shadowBlur = 15;
                    } else if (type === 'golden') {
                        ctx.shadowColor = 'gold';
                        ctx.shadowBlur = 20;
                    }"""
    content = content.replace(draw_shadow_search, draw_shadow_replace)

    # 3. Update trySlap (rewards)
    tryslap_search = """                        // Add float text
                        if (isPerfect) {
                            gameData.coins += 2;
                            gameData.stats.totalCoinsEarned += 2;
                            addFloatText('PERFECT! +2💰' + comboText, c.x, c.y - 10);
                            spawnImpact(c.x, c.y, true);
                            playSound(850, 0.15);
                            triggerShake(6, 0.2);
                            triggerFlash(0.15, '#fff');
                            hitStop = 0.15;
                            spawnRoseExplosion(c.x, c.y);
                        } else {
                            gameData.coins += 1;
                            gameData.stats.totalCoinsEarned += 1;
                            addFloatText('SLAP! +1💰' + comboText, c.x, c.y);
                            spawnImpact(c.x, c.y);
                            playSound(600, 0.1);
                        }"""
    tryslap_replace = """                        // Add float text
                        if (c.type === 'golden') {
                            if (isPerfect) {
                                gameData.coins += 25;
                                gameData.stats.totalCoinsEarned += 25;
                                score += 500;
                                addFloatText('JACKPOT! +25💰' + comboText, c.x, c.y - 10, 'gold', 20);
                                spawnImpact(c.x, c.y, true);
                                playSound(850, 0.3);
                                triggerShake(15, 0.4);
                                triggerFlash(0.3, 'gold');
                                hitStop = 0.2;
                                spawnRoseExplosion(c.x, c.y);
                            } else {
                                gameData.coins += 10;
                                gameData.stats.totalCoinsEarned += 10;
                                score += 100;
                                addFloatText('GOLDEN SLAP! +10💰' + comboText, c.x, c.y, 'gold', 16);
                                spawnImpact(c.x, c.y);
                                playSound(600, 0.2);
                            }
                        } else if (isPerfect) {
                            gameData.coins += 2;
                            gameData.stats.totalCoinsEarned += 2;
                            addFloatText('PERFECT! +2💰' + comboText, c.x, c.y - 10);
                            spawnImpact(c.x, c.y, true);
                            playSound(850, 0.15);
                            triggerShake(6, 0.2);
                            triggerFlash(0.15, '#fff');
                            hitStop = 0.15;
                            spawnRoseExplosion(c.x, c.y);
                        } else {
                            gameData.coins += 1;
                            gameData.stats.totalCoinsEarned += 1;
                            addFloatText('SLAP! +1💰' + comboText, c.x, c.y);
                            spawnImpact(c.x, c.y);
                            playSound(600, 0.1);
                        }"""
    content = content.replace(tryslap_search, tryslap_replace)

    # 4. updateChanclas hit damage against boss
    hitboss_search = """                            let damage = c.type === 'super' ? 15 : (c.type === 'fire' ? 12 : 8);"""
    hitboss_replace = """                            let damage = c.type === 'super' ? 15 : (c.type === 'fire' ? 12 : (c.type === 'golden' ? 25 : 8));"""
    content = content.replace(hitboss_search, hitboss_replace)

    with open(filename, 'w') as f:
        f.write(content)

update_file('index.html')
update_file('chancla_bomb.html')
