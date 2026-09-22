import re
def modify_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    spawn_pattern = r"(const isSniper = [^\n]+;)(\n\s*const isFire = [^\n]+;)"
    spawn_replacement = r"\1\n                const isGhost = !isBomb && !isHoming && !isSuper && !isGolden && !isBoomerang && !isTrick && !isSniper && Math.random() < 0.15;\2"
    content = re.sub(spawn_pattern, spawn_replacement, content)

    fire_pattern = r"(const isFire = isa.enraged && !isBomb && !isHoming && !isSuper && !isGolden && !isBoomerang && !isTrick && !isSniper)( && Math.random\(\) < 0.25;)"
    content = re.sub(fire_pattern, r"\1 && !isGhost\2", content)

    size_pattern = r"(else if \(isSniper\) \{ w = 34; h = 24; \})"
    content = re.sub(size_pattern, r"\1\n                else if (isGhost) { w = 36; h = 22; }", content)

    type_str_pattern = r"(else if \(isSniper\) type = 'sniper';)"
    content = re.sub(type_str_pattern, r"\1\n                else if (isGhost) type = 'ghost';", content)

    push_pattern = r"(chanclas.push\(\{ x, y, vx, vy, w, h, type, rotation: 0, rotSpeed, trickState: 0, trickTimer: 0,\n\s*sniperTimer: isSniper \? 1.5 : 0)(\s*\}\);)"
    content = re.sub(push_pattern, r"\1, invisible: false, dodged: false, returning: false\2", content)

    update_chancla_pattern = r"(const currentDt = c.slapped \? dt : enemyDt;\n\s*c.x \+= c.vx \* currentDt;)"
    ghost_logic = r'''
                    // Ghost Logic
                    if (c.type === 'ghost' && !c.slapped) {
                        if (c.y > canvas.height * 0.25 && c.y < canvas.height * 0.75) {
                            c.invisible = true;
                        } else {
                            c.invisible = false;
                        }
                    } else if (c.slapped) {
                        c.invisible = false;
                    }

                    \1'''
    content = re.sub(update_chancla_pattern, ghost_logic, content)

    try_slap_pattern = r"(else if \(c.type === 'trick'\) \{[\s\S]*?if \(isa.anger <= 0\) triggerWin\(\);\n\s*\})"
    ghost_reward = r'''\1 else if (c.type === 'ghost') {
                            gameData.coins += Math.floor(5 * getPrestigeMultiplier());
                            gameData.stats.totalCoinsEarned += Math.floor(5 * getPrestigeMultiplier());
                            score += Math.floor(150 * getPrestigeMultiplier());
                            addFloatText('GHOST BUSTED! 👻', c.x, c.y, '#ffffff');
                        }'''
    content = re.sub(try_slap_pattern, ghost_reward, content)

    draw_all_pattern = r"(for \(const c of chanclas\) drawChancla\(ctx, c.x, c.y, c.w, c.h, c.type, c.rotation)(\);)"
    content = re.sub(draw_all_pattern, r"\1, c\2", content)

    draw_sig_pattern = r"(function drawChancla\(ctx, x, y, w, h, type, rotation)(\) \{)"
    content = re.sub(draw_sig_pattern, r"\1, c\2", content)

    # Only add to drawChancla specifically
    content = re.sub(r"(function drawChancla\(ctx, x, y, w, h, type, rotation, c\) \{\s*ctx.save\(\);)", r"\1\n                if (c && c.invisible) {\n                    ctx.globalAlpha = 0;\n                }", content)

    draw_emoji_pattern = r"(else if \(type === 'sniper'\) emoji = '🎯';)"
    content = re.sub(draw_emoji_pattern, r"\1\n                else if (type === 'ghost') emoji = '👻';", content)

    storm_func = r'''
            function triggerChanclaStorm() {
                addFloatText('CHANCLA STORM! 🌪️', isa.x, isa.y + 30, '#ff4d4d', 20);
                playSound(1000, 0.6);
                triggerShake(20, 1.0);

                for (let i = 0; i < 15; i++) {
                    const angle = (Math.PI / 14) * i;
                    const speed = baseSpeed + 150 + Math.random() * 50;
                    chanclas.push({
                        x: isa.x,
                        y: isa.y,
                        vx: Math.cos(angle) * speed,
                        vy: Math.sin(angle) * speed,
                        w: 32,
                        h: 18,
                        type: 'fire',
                        rotation: 0,
                        rotSpeed: (Math.random() - 0.5) * 15,
                        trickState: 0,
                        trickTimer: 0,
                        sniperTimer: 0,
                        invisible: false,
                        dodged: false,
                        returning: false
                    });
                }
            }
'''
    content = re.sub(r"(function spawnMeteor\(\) \{)", storm_func + r"\n            \1", content)

    enraged_call = r"(addFloatText\('¡ENRAGED!', isa.x, isa.y - 30\);\n\s*\})"
    content = re.sub(enraged_call, r"addFloatText('¡ENRAGED!', isa.x, isa.y - 30);\n                        triggerChanclaStorm();\n                    }", content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

modify_file('index.html')
modify_file('chancla_bomb.html')
