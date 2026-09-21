import re

def update_file(filename):
    with open(filename, 'r') as f:
        content = f.read()

    # 1. Update drawChancla signature
    content = re.sub(
        r'function drawChancla\(ctx, x, y, w, h, type, rotation\) {',
        r'function drawChancla(ctx, x, y, w, h, type, rotation, c) {',
        content
    )

    # 2. Update drawChanclasAll
    content = re.sub(
        r'for \(const c of chanclas\) drawChancla\(ctx, c\.x, c\.y, c\.w, c\.h, c\.type, c\.rotation\);',
        r'for (const c of chanclas) drawChancla(ctx, c.x, c.y, c.w, c.h, c.type, c.rotation, c);',
        content
    )

    # 3. Add isGhost in spawnChancla
    content = re.sub(
        r'(const isFire = isa\.enraged && !isBomb && !isHoming && !isSuper && !isGolden && !isBoomerang && !isTrick && !isSniper && Math\.random\(\) < 0\.25;)',
        r'\1\n                const isGhost = !isBomb && !isHoming && !isSuper && !isGolden && !isBoomerang && !isTrick && !isSniper && !isFire && Math.random() < 0.15;',
        content
    )

    content = re.sub(
        r'(else if \(isSniper\) type = \'sniper\';)',
        r'\1\n                else if (isGhost) type = \'ghost\';',
        content
    )

    content = re.sub(
        r'(sniperTimer: isSniper \? 1\.5 : 0) }',
        r'\1, invisible: false }',
        content
    )

    # 4. updateChanclas logic
    trick_logic = r'(if \(c\.type === \'trick\' && !c\.slapped\) {.*?^                    })'
    replacement_logic = r'''\1

                    if (c.type === 'ghost' && !c.slapped) {
                        if (c.y > canvas.height * 0.25 && c.y < canvas.height * 0.75) {
                            c.invisible = true;
                        } else {
                            c.invisible = false;
                        }
                    }'''
    content = re.sub(trick_logic, replacement_logic, content, flags=re.MULTILINE | re.DOTALL)

    # 5. Emoji and Invisibility in drawChancla
    content = re.sub(
        r'(else if \(type === \'sniper\'\) emoji = \'🎯\';)',
        r'\1\n                else if (type === \'ghost\') emoji = \'👻\';',
        content
    )

    content = re.sub(
        r'(if \(type === \'sniper\' && !c\.slapped && c\.sniperTimer > 0\))',
        r'if (type === \'sniper\' && c && !c.slapped && c.sniperTimer > 0)',
        content
    )

    content = re.sub(
        r'(ctx\.font = `\$\{Math\.max\(28, w \* 1\.4\)\}px \'Noto Color Emoji\', \'Apple Color Emoji\', \'Segoe UI Emoji\', sans-serif`;)',
        r'if (c && c.invisible) {\n                        ctx.globalAlpha = 0;\n                    }\n                    \1',
        content
    )

    # 6. trySlap logic
    try_slap_trick = r'(} else if \(c\.type === \'trick\'\) {.*?if \(isa\.anger <= 0\) triggerWin\(\);)'
    try_slap_ghost = r'''\1
                        } else if (c.type === 'ghost') {
                            gameData.coins += Math.floor(5 * getPrestigeMultiplier());
                            gameData.stats.totalCoinsEarned += Math.floor(5 * getPrestigeMultiplier());
                            score += Math.floor(150 * getPrestigeMultiplier());
                            addFloatText('GHOST BUSTED! 👻', c.x, c.y);
                            spawnImpact(c.x, c.y);
                            playSound(850, 0.15);'''
    content = re.sub(try_slap_trick, try_slap_ghost, content, flags=re.MULTILINE | re.DOTALL)

    with open(filename, 'w') as f:
        f.write(content)

update_file('index.html')
update_file('chancla_bomb.html')
print("Ghost chancla injected successfully.")
