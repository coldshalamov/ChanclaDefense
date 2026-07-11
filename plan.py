import os

def apply_changes(filename):
    with open(filename, 'r') as f:
        content = f.read()

    # Step 2
    content = content.replace('''                const isSuper = superEnabled && !isBomb && !isHoming && Math.random() < 0.18;
                const isFire = isa.enraged && !isBomb && !isHoming && !isSuper && Math.random() < 0.25;

                let w = 32;
                let h = 18;
                if (isSuper) { w = 46; h = 26; }
                else if (isBomb) { w = 38; h = 38; }
                else if (isHoming) { w = 36; h = 36; }''', '''                const isBlackHole = timeElapsed > 30 && !isBomb && !isHoming && Math.random() < 0.05;
                const isSuper = superEnabled && !isBomb && !isHoming && !isBlackHole && Math.random() < 0.18;
                const isFire = isa.enraged && !isBomb && !isHoming && !isSuper && !isBlackHole && Math.random() < 0.25;

                let w = 32;
                let h = 18;
                if (isBlackHole) { w = 40; h = 40; }
                else if (isSuper) { w = 46; h = 26; }
                else if (isBomb) { w = 38; h = 38; }
                else if (isHoming) { w = 36; h = 36; }''')

    content = content.replace('''                let vy = baseSpeed + Math.random() * 60;
                if (isSuper) vy += 40;
                else if (isFire) vy += 80;
                else if (isBomb) vy = baseSpeed * 0.7 + Math.random() * 30; // slower
                else if (isHoming) vy = baseSpeed * 0.8; // slightly slower vertical speed''', '''                let vy = baseSpeed + Math.random() * 60;
                if (isBlackHole) vy = baseSpeed * 0.4;
                else if (isSuper) vy += 40;
                else if (isFire) vy += 80;
                else if (isBomb) vy = baseSpeed * 0.7 + Math.random() * 30; // slower
                else if (isHoming) vy = baseSpeed * 0.8; // slightly slower vertical speed''')

    content = content.replace('''                let type = 'normal';
                if (isBomb) type = 'bomb';
                else if (isFire) type = 'fire';
                else if (isSuper) type = 'super';
                else if (isHoming) type = 'homing';''', '''                let type = 'normal';
                if (isBlackHole) type = 'blackhole';
                else if (isBomb) type = 'bomb';
                else if (isFire) type = 'fire';
                else if (isSuper) type = 'super';
                else if (isHoming) type = 'homing';''')


    # Step 3
    content = content.replace('''                let emoji = '🩴💨';
                if (type === 'super') emoji = '🩴💥';
                else if (type === 'fire') emoji = '🔥';
                else if (type === 'bomb') emoji = '💣';
                else if (type === 'homing') emoji = '🪬';''', '''                let emoji = '🩴💨';
                if (type === 'blackhole') emoji = '🌌';
                else if (type === 'super') emoji = '🩴💥';
                else if (type === 'fire') emoji = '🔥';
                else if (type === 'bomb') emoji = '💣';
                else if (type === 'homing') emoji = '🪬';''')

    content = content.replace('''                    } else if (type === 'homing') {
                        ctx.shadowColor = '#8a2be2';
                        ctx.shadowBlur = 15;
                    }''', '''                    } else if (type === 'homing') {
                        ctx.shadowColor = '#8a2be2';
                        ctx.shadowBlur = 15;
                    } else if (type === 'blackhole') {
                        ctx.shadowColor = '#ffffff';
                        ctx.shadowBlur = 25;
                        ctx.fillStyle = 'rgba(0,0,0,0.5)';
                        ctx.beginPath();
                        ctx.arc(0, h * 0.2, w * 0.8, 0, Math.PI * 2);
                        ctx.fill();
                    }''')


    # Step 4
    content = content.replace('''                    // Homing Logic
                    if (c.type === 'homing' && !c.slapped) {''', '''                    // Black Hole Logic
                    if (c.type === 'blackhole' && !c.slapped) {
                        for (let j = chanclas.length - 1; j >= 0; j--) {
                            if (i === j) continue;
                            const other = chanclas[j];
                            if (other.type !== 'meteor' && other.type !== 'blackhole' && !other.slapped) {
                                const dist = Math.sqrt(Math.pow(c.x - other.x, 2) + Math.pow(c.y - other.y, 2));
                                if (dist < 180) {
                                    other.vx += (c.x - other.x) * 4 * dt;
                                    other.vy += (c.y - other.y) * 4 * dt;
                                    if (dist < c.w / 2) {
                                        chanclas.splice(j, 1);
                                        c.absorbed = (c.absorbed || 0) + 1;
                                        addFloatText('SLURP!', c.x, c.y, '#9c27b0', 12);
                                        if (j < i) i--; // Adjust index
                                    }
                                }
                            }
                        }
                    }

                    // Homing Logic
                    if (c.type === 'homing' && !c.slapped) {''')

    content = content.replace('''                    if (!c.slapped && c.type !== 'meteor' && rectsOverlap(player, c)) {
                        if (c.isShrapnel && c.vy < 0) continue; // Don't hurt player if flying upwards
                        if (dashTimer > 0) continue; // I-frames during dash''', '''                    let effectiveC = c;
                    if (c.type === 'blackhole') {
                        effectiveC = { x: c.x + c.w/4, y: c.y + c.h/4, w: c.w/2, h: c.h/2 }; // smaller hitbox for player
                    }
                    if (!c.slapped && c.type !== 'meteor' && rectsOverlap(player, effectiveC)) {
                        if (c.isShrapnel && c.vy < 0) continue; // Don't hurt player if flying upwards
                        if (dashTimer > 0) continue; // I-frames during dash''')

    # Step 5
    content = content.replace('''                        const isPerfect = dist < perfectRange;

                        gameData.stats.totalSlaps++;
                        if (isPerfect) gameData.stats.perfectSlaps++;''', '''                        const isPerfect = dist < perfectRange;

                        gameData.stats.totalSlaps++;
                        if (isPerfect) gameData.stats.perfectSlaps++;

                        if (c.type === 'blackhole') {
                            c.slapped = true;
                            // Galaxy Burst!
                            const numShards = (c.absorbed || 0) + 3;
                            for(let s=0; s<numShards; s++) {
                                const angle = Math.PI * (1.2 + Math.random() * 0.6); // Upwards arc
                                const speed = 300 + Math.random() * 200;
                                chanclas.push({
                                    x: c.x, y: c.y,
                                    vx: Math.cos(angle) * speed,
                                    vy: Math.sin(angle) * speed,
                                    w: 32, h: 18, type: 'fire', rotation: 0, rotSpeed: (Math.random() - 0.5) * 15,
                                    slapped: true, // Already slapped so it hurts Isa
                                    isShrapnel: true
                                });
                            }
                            triggerShake(30, 0.6);
                            triggerFlash(0.4, '#e0b0ff');
                            addFloatText('GALAXY BURST! 🌌', c.x, c.y - 40);
                            playSound(1200, 0.4);
                            chanclas.splice(i, 1);
                            slappedAny = true;
                            continue;
                        }''')

    with open(filename, 'w') as f:
        f.write(content)

apply_changes('index.html')
apply_changes('chancla_bomb.html')
