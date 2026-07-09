import re

def update_file(filename):
    with open(filename, "r") as f:
        content = f.read()

    # 1. spawnChancla
    spawn_orig = """            function spawnChancla() {
                const isBomb = Math.random() < 0.08;
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
                else if (isHoming) type = 'homing';

                chanclas.push({ x, y, vx, vy, w, h, type, rotation: 0, rotSpeed });
                if (isSuper) sayPlayer('super');
            }"""

    spawn_new = """            function spawnChancla() {
                const isBomb = Math.random() < 0.08;
                const isGhost = !isBomb && Math.random() < 0.12;
                const isHoming = superEnabled && !isBomb && !isGhost && Math.random() < 0.10;
                const isSuper = superEnabled && !isBomb && !isGhost && !isHoming && Math.random() < 0.18;
                const isFire = isa.enraged && !isBomb && !isGhost && !isHoming && !isSuper && Math.random() < 0.25;

                let w = 32;
                let h = 18;
                if (isSuper) { w = 46; h = 26; }
                else if (isBomb) { w = 38; h = 38; }
                else if (isHoming) { w = 36; h = 36; }
                else if (isGhost) { w = 34; h = 34; }

                const x = 40 + Math.random() * (canvas.width - 80);
                const y = isa.y + 40;

                let vy = baseSpeed + Math.random() * 60;
                if (isSuper) vy += 40;
                else if (isFire) vy += 80;
                else if (isBomb) vy = baseSpeed * 0.7 + Math.random() * 30; // slower
                else if (isHoming) vy = baseSpeed * 0.8; // slightly slower vertical speed
                else if (isGhost) vy = baseSpeed * 0.85;

                const vx = (Math.random() - 0.5) * 60;
                const rotSpeed = (Math.random() - 0.5) * 5;

                let type = 'normal';
                if (isBomb) type = 'bomb';
                else if (isFire) type = 'fire';
                else if (isSuper) type = 'super';
                else if (isHoming) type = 'homing';
                else if (isGhost) type = 'ghost';

                chanclas.push({ x, y, vx, vy, w, h, type, rotation: 0, rotSpeed, invisible: false });
                if (isSuper) sayPlayer('super');
            }"""
    content = content.replace(spawn_orig, spawn_new)

    # 2. updateChanclas Ghost logic
    update_orig = """                    // Homing Logic
                    if (c.type === 'homing' && !c.slapped) {"""
    update_new = """                    // Ghost Logic
                    if (c.type === 'ghost' && !c.slapped) {
                        if (c.y > canvas.height * 0.4) {
                            c.invisible = true;
                        }
                    }

                    // Homing Logic
                    if (c.type === 'homing' && !c.slapped) {"""
    content = content.replace(update_orig, update_new)

    # 3. drawChanclasAll
    draw_all_orig = """            function drawChanclasAll() {
                for (const c of chanclas) drawChancla(ctx, c.x, c.y, c.w, c.h, c.type, c.rotation);
            }"""
    draw_all_new = """            function drawChanclasAll() {
                for (const c of chanclas) {
                    if (c.invisible) continue;
                    drawChancla(ctx, c.x, c.y, c.w, c.h, c.type, c.rotation);
                }
            }"""
    content = content.replace(draw_all_orig, draw_all_new)

    # 4. drawChancla emoji
    emoji_orig = """                else if (type === 'bomb') emoji = '💣';
                else if (type === 'homing') emoji = '🪬';"""
    emoji_new = """                else if (type === 'bomb') emoji = '💣';
                else if (type === 'homing') emoji = '🪬';
                else if (type === 'ghost') emoji = '👻';"""
    content = content.replace(emoji_orig, emoji_new)

    # 5. trySlap text & points
    slap_orig = """                    if (dist < slapRange) {
                        // Slap the chancla away
                        const isPerfect = dist < perfectRange;

                        gameData.stats.totalSlaps++;"""
    slap_new = """                    if (dist < slapRange) {
                        // Slap the chancla away
                        const isPerfect = dist < perfectRange;

                        if (c.type === 'ghost' && c.invisible) {
                            c.invisible = false;
                            score += 20;
                            addFloatText('GHOST BUSTED! 👻', c.x, c.y - 50, '#ff00ff');
                        }

                        gameData.stats.totalSlaps++;"""
    content = content.replace(slap_orig, slap_new)

    # 6. trySlap hit Isa damage
    dmg_orig = """                            let damage = c.type === 'super' ? 15 : (c.type === 'fire' ? 12 : 8);
                            if (c.rallyCount > 0) damage += 10 * c.rallyCount;
                            if (c.type === 'meteor') damage = 40;
                            if (c.type === 'bomb') damage = 20;
                            if (c.isPerfect) damage += 7;"""
    dmg_new = """                            let damage = c.type === 'super' ? 15 : (c.type === 'fire' ? 12 : 8);
                            if (c.rallyCount > 0) damage += 10 * c.rallyCount;
                            if (c.type === 'meteor') damage = 40;
                            if (c.type === 'bomb') damage = 20;
                            if (c.type === 'ghost') damage = 10;
                            if (c.isPerfect) damage += 7;"""
    content = content.replace(dmg_orig, dmg_new)

    # 7. trySlap hit player damage
    player_dmg_orig = """                        const dmg = (c.type === 'super' || c.type === 'fire' || c.type === 'bomb') ? 2 : 1;
                        comboCount = 0;
                        const shakeAmt = c.type === 'bomb' ? 20 : (c.type === 'super' || c.type === 'fire' ? 15 : 8);"""
    player_dmg_new = """                        const dmg = (c.type === 'super' || c.type === 'fire' || c.type === 'bomb') ? 2 : 1;
                        comboCount = 0;
                        const shakeAmt = c.type === 'bomb' ? 20 : (c.type === 'super' || c.type === 'fire' ? 15 : 8);
                        if (c.type === 'ghost') c.invisible = false;"""
    content = content.replace(player_dmg_orig, player_dmg_new)

    with open(filename, "w") as f:
        f.write(content)

update_file("index.html")
update_file("chancla_bomb.html")
