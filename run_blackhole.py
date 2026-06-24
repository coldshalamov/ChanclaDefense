import re

def process(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # 1. Add `isBlackhole` in `spawnChancla()`
    spawn_search = """                const isFire = isa.enraged && !isBomb && !isHoming && !isSuper && Math.random() < 0.25;"""
    spawn_replace = """                const isFire = isa.enraged && !isBomb && !isHoming && !isSuper && Math.random() < 0.25;
                const isBlackhole = !isBomb && !isHoming && !isSuper && !isFire && Math.random() < 0.05;"""
    content = content.replace(spawn_search, spawn_replace)

    size_search = """                if (isSuper) { w = 46; h = 26; }
                else if (isBomb) { w = 38; h = 38; }
                else if (isHoming) { w = 36; h = 36; }"""
    size_replace = """                if (isSuper) { w = 46; h = 26; }
                else if (isBomb) { w = 38; h = 38; }
                else if (isHoming) { w = 36; h = 36; }
                else if (isBlackhole) { w = 40; h = 40; }"""
    content = content.replace(size_search, size_replace)

    vy_search = """                else if (isBomb) vy = baseSpeed * 0.7 + Math.random() * 30; // slower
                else if (isHoming) vy = baseSpeed * 0.8; // slightly slower vertical speed"""
    vy_replace = """                else if (isBomb) vy = baseSpeed * 0.7 + Math.random() * 30; // slower
                else if (isHoming) vy = baseSpeed * 0.8; // slightly slower vertical speed
                else if (isBlackhole) vy = baseSpeed * 0.4; // slowly falls downwards"""
    content = content.replace(vy_search, vy_replace)

    type_search = """                if (isBomb) type = 'bomb';
                else if (isFire) type = 'fire';
                else if (isSuper) type = 'super';
                else if (isHoming) type = 'homing';"""
    type_replace = """                if (isBomb) type = 'bomb';
                else if (isFire) type = 'fire';
                else if (isSuper) type = 'super';
                else if (isHoming) type = 'homing';
                else if (isBlackhole) type = 'blackhole';"""
    content = content.replace(type_search, type_replace)

    # 2. Add Emoji in `drawChancla`
    emoji_search = """                else if (type === 'homing') emoji = '🪬';"""
    emoji_replace = """                else if (type === 'homing') emoji = '🪬';
                else if (type === 'blackhole') emoji = '🌌';"""
    content = content.replace(emoji_search, emoji_replace)

    # 3. Add shadow in `drawChancla`
    shadow_search = """                    } else if (type === 'homing') {
                        ctx.shadowColor = '#8a2be2';
                        ctx.shadowBlur = 15;
                    }"""
    shadow_replace = """                    } else if (type === 'homing') {
                        ctx.shadowColor = '#8a2be2';
                        ctx.shadowBlur = 15;
                    } else if (type === 'blackhole') {
                        ctx.shadowColor = '#4b0082';
                        ctx.shadowBlur = 25;
                    }"""
    content = content.replace(shadow_search, shadow_replace)

    # 4. Add Black Hole collision and logic in `updateChanclas` loop
    # We find where we do `c.x += c.vx * dt;`
    loop_search = """                    c.x += c.vx * dt;
                    c.y += c.vy * dt;"""
    loop_replace = """                    if (c.type === 'blackhole' && !c.slapped) {
                        for (let j = 0; j < chanclas.length; j++) {
                            if (i === j) continue;
                            const other = chanclas[j];
                            if (!other.slapped && other.type !== 'meteor' && other.type !== 'blackhole') {
                                const dist = Math.sqrt(Math.pow(c.x - other.x, 2) + Math.pow(c.y - other.y, 2));
                                if (dist < 180) {
                                    // Sucks it in
                                    const pullX = (c.x - other.x) * 2 * dt;
                                    const pullY = (c.y - other.y) * 2 * dt;
                                    other.x += pullX;
                                    other.y += pullY;
                                    if (dist < 20) {
                                        // Absorb
                                        c.absorbed = (c.absorbed || 0) + 1;
                                        chanclas.splice(j, 1);
                                        // Adjust index since we removed an element
                                        if (j < i) i--;
                                        j--;
                                        addFloatText('+1 🌌', c.x, c.y, '#d8b4e2');
                                    }
                                }
                            }
                        }
                    }

                    c.x += c.vx * dt;
                    c.y += c.vy * dt;"""
    content = content.replace(loop_search, loop_replace)

    # 5. Add Player hit detection with hitbox adjustment in `updateChanclas`
    hitbox_search_better = """                    if (!c.slapped && c.type !== 'meteor' && rectsOverlap(player, c)) {"""
    hitbox_replace_better = """                    let overlapTarget = c;
                    if (c.type === 'blackhole') {
                        overlapTarget = { x: c.x + c.w/4, y: c.y + c.h/4, w: c.w/2, h: c.h/2 };
                    }
                    if (!c.slapped && c.type !== 'meteor' && rectsOverlap(player, overlapTarget)) {"""
    content = content.replace(hitbox_search_better, hitbox_replace_better)

    # 6. Add GALAXY BURST in `trySlap` -> inside `if (dist < slapRange)`
    slap_search = """                        c.vx = (c.x - player.x) * (isPerfect ? 12 : 8);
                        c.vy = isPerfect ? -550 : -300;
                        c.slapped = true;
                        c.isPerfect = isPerfect;
                        c.rotSpeed = (Math.random() < 0.5 ? -1 : 1) * (isPerfect ? 35 : 15 + Math.random() * 10);
                        slappedAny = true;"""
    slap_replace = """                        c.vx = (c.x - player.x) * (isPerfect ? 12 : 8);
                        c.vy = isPerfect ? -550 : -300;
                        c.slapped = true;
                        c.isPerfect = isPerfect;
                        c.rotSpeed = (Math.random() < 0.5 ? -1 : 1) * (isPerfect ? 35 : 15 + Math.random() * 10);
                        slappedAny = true;

                        if (c.type === 'blackhole') {
                            addFloatText('GALAXY BURST!', c.x, c.y - 20, '#d8b4e2');
                            triggerShake(20, 0.4);
                            triggerFlash(0.2, '#4b0082');
                            playSound(1200, 0.5);
                            const burstCount = (c.absorbed || 0) + 3;
                            for (let b = 0; b < burstCount; b++) {
                                chanclas.push({
                                    x: c.x,
                                    y: c.y,
                                    vx: (Math.random() - 0.5) * 400,
                                    vy: -400 - Math.random() * 300,
                                    w: 32, h: 18,
                                    type: 'fire',
                                    rotation: Math.random() * Math.PI * 2,
                                    rotSpeed: (Math.random() - 0.5) * 20,
                                    slapped: true,
                                    isPerfect: true
                                });
                            }
                            chanclas.splice(i, 1);
                            continue;
                        }"""
    content = content.replace(slap_search, slap_replace)

    print(f"Modifying {filepath}")
    with open(filepath, 'w') as f:
        f.write(content)

process('index.html')
process('chancla_bomb.html')
