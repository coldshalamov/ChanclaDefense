def update_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    content = content.replace(
        '''            function drawChancla(ctx, x, y, w, h, type, rotation) {
                ctx.save();
                ctx.translate(x, y);''',
        '''            function drawChancla(ctx, x, y, w, h, type, rotation, c) {
                ctx.save();
                if (c && c.invisible) ctx.globalAlpha = 0;
                ctx.translate(x, y);'''
    )

    content = content.replace(
        '''                else if (type === 'trick') emoji = '🃏';
                else if (type === 'sniper') emoji = '🎯';''',
        '''                else if (type === 'trick') emoji = '🃏';
                else if (type === 'sniper') emoji = '🎯';
                else if (type === 'ghost') emoji = '👻';'''
    )

    content = content.replace(
        '''            function drawChanclasAll() {
                for (const c of chanclas) drawChancla(ctx, c.x, c.y, c.w, c.h, c.type, c.rotation);
            }''',
        '''            function drawChanclasAll() {
                for (const c of chanclas) drawChancla(ctx, c.x, c.y, c.w, c.h, c.type, c.rotation, c);
            }'''
    )

    content = content.replace(
        '''                const isSniper = !isBomb && !isHoming && !isSuper && !isGolden && !isBoomerang && !isTrick && Math.random() < 0.12;
                const isFire = isa.enraged && !isBomb && !isHoming && !isSuper && !isGolden && !isBoomerang && !isTrick && !isSniper && Math.random() < 0.25;''',
        '''                const isSniper = !isBomb && !isHoming && !isSuper && !isGolden && !isBoomerang && !isTrick && Math.random() < 0.12;
                const isFire = isa.enraged && !isBomb && !isHoming && !isSuper && !isGolden && !isBoomerang && !isTrick && !isSniper && Math.random() < 0.25;
                const isGhost = !isBomb && !isHoming && !isSuper && !isGolden && !isBoomerang && !isTrick && !isSniper && !isFire && Math.random() < 0.15;'''
    )

    content = content.replace(
        '''                else if (isBoomerang) { w = 38; h = 22; }
                else if (isTrick) { w = 36; h = 22; }
                else if (isSniper) { w = 34; h = 24; }''',
        '''                else if (isBoomerang) { w = 38; h = 22; }
                else if (isTrick) { w = 36; h = 22; }
                else if (isSniper) { w = 34; h = 24; }
                else if (isGhost) { w = 36; h = 24; }'''
    )

    content = content.replace(
        '''                else if (isBoomerang) vy = baseSpeed * 1.2; // faster down
                else if (isTrick) vy = baseSpeed * 0.9;
                else if (isSniper) vy = 0;''',
        '''                else if (isBoomerang) vy = baseSpeed * 1.2; // faster down
                else if (isTrick) vy = baseSpeed * 0.9;
                else if (isSniper) vy = 0;
                else if (isGhost) vy = baseSpeed * 1.1;'''
    )

    content = content.replace(
        '''                else if (isTrick) type = 'trick';
                else if (isSniper) type = 'sniper';''',
        '''                else if (isTrick) type = 'trick';
                else if (isSniper) type = 'sniper';
                else if (isGhost) type = 'ghost';'''
    )

    content = content.replace(
        '''                chanclas.push({ x, y, vx, vy, w, h, type, rotation: 0, rotSpeed, trickState: 0, trickTimer: 0,
                    sniperTimer: isSniper ? 1.5 : 0 });''',
        '''                chanclas.push({ x, y, vx, vy, w, h, type, rotation: 0, rotSpeed, trickState: 0, trickTimer: 0,
                    sniperTimer: isSniper ? 1.5 : 0, invisible: false });'''
    )

    ghost_logic = '''                    // Ghost Logic
                    if (c.type === 'ghost' && !c.slapped) {
                        if (c.y > canvas.height * 0.25 && c.y < canvas.height * 0.75) {
                            c.invisible = true;
                        } else {
                            c.invisible = false;
                        }
                    }

                    // Homing Logic'''
    content = content.replace(
        "                    // Homing Logic",
        ghost_logic
    )

    ghost_slap = '''                        } else if (c.type === 'ghost') {
                            gameData.coins += Math.floor(5 * getPrestigeMultiplier());
                            gameData.stats.totalCoinsEarned += Math.floor(5 * getPrestigeMultiplier());
                            score += Math.floor(150 * getPrestigeMultiplier());
                            addFloatText('GHOST BUSTED! 👻', c.x, c.y, '#fff');
                            spawnImpact(c.x, c.y, true);
                            playSound(850, 0.15);
                        } else if (isPerfect) {'''
    content = content.replace(
        "                        } else if (isPerfect) {",
        ghost_slap
    )

    with open(filepath, 'w') as f:
        f.write(content)

for file in ['index.html', 'chancla_bomb.html']:
    update_file(file)
