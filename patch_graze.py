import sys

def modify_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # 1. Add triggerGraze function
    trigger_graze_code = """
            function triggerGraze(c, text) {
                specialAttackBar = Math.min(maxSpecialAttack, specialAttackBar + 10);
                score += 15;
                addFloatText(text, player.x, player.y - 40, '#00ffcc', 14);
                playSound(2000, 0.1);

                if (!specialReadyTriggered && specialAttackBar >= maxSpecialAttack) {
                    specialReadyTriggered = true;
                    const eggX = canvas.width / 2;
                    const eggY = 50;
                    spawnImpact(eggX, eggY, true);
                    for (let k = 0; k < 8; k++) {
                        rosePetals.push({
                            x: eggX, y: eggY,
                            vx: (Math.random() - 0.5) * 200, vy: (Math.random() - 0.5) * 200,
                            rotation: Math.random() * 6, rotSpeed: Math.random() * 10,
                            emoji: '✨', size: 20
                        });
                    }
                    playSound(1200, 0.25);
                    triggerShake(5, 0.2);
                }
            }
"""

    # Insert after rectsOverlap
    search_rects = "            function rectsOverlap(a, b) {\n                return Math.abs(a.x - b.x) < (a.w / 2 + b.w / 2) && Math.abs(a.y - b.y) < (a.h / 2 + b.h / 2);\n            }"
    if search_rects in content:
        content = content.replace(search_rects, search_rects + "\n" + trigger_graze_code)
    else:
        print(f"Error: rectsOverlap not found in {filepath}")

    # 2. Modify updateChanclas logic
    search_logic = """                    if (!c.slapped && c.type !== 'meteor' && rectsOverlap(player, c)) {
                        if (c.isShrapnel && c.vy < 0) continue; // Don't hurt player if flying upwards
                        if (dashTimer > 0) continue; // I-frames during dash"""
    replace_logic = """                    if (!c.slapped && c.type !== 'meteor') {
                        if (rectsOverlap(player, c)) {
                            if (c.isShrapnel && c.vy < 0) continue; // Don't hurt player if flying upwards
                            if (dashTimer > 0) {
                                if (!c.grazed) {
                                    c.grazed = true;
                                    triggerGraze(c, 'PERFECT DODGE!');
                                }
                                continue; // I-frames during dash
                            }"""

    if search_logic in content:
        content = content.replace(search_logic, replace_logic)
    else:
        print(f"Error: search_logic not found in {filepath}")

    search_hit_end = """                        if (player.lives <= 0) {
                            endGame();
                            return;
                        }"""
    replace_hit_end = """                        if (player.lives <= 0) {
                            endGame();
                            return;
                        }
                        } else if (!c.grazed) {
                            const grazeDistX = player.w / 2 + c.w / 2 + 25;
                            const grazeDistY = player.h / 2 + c.h / 2 + 25;
                            if (Math.abs(player.x - c.x) < grazeDistX && Math.abs(player.y - c.y) < grazeDistY) {
                                if (!(c.isShrapnel && c.vy < 0)) {
                                    c.grazed = true;
                                    triggerGraze(c, 'GRAZE!');
                                }
                            }
                        }"""

    if search_hit_end in content:
        content = content.replace(search_hit_end, replace_hit_end)
    else:
        print(f"Error: search_hit_end not found in {filepath}")

    search_meteor = """                    } else if (!c.slapped && c.type === 'meteor' && c.y > canvas.height - 100) {
                        if (dashTimer > 0) continue; // I-frames during dash shockwave"""
    replace_meteor = """                    } else if (!c.slapped && c.type === 'meteor' && c.y > canvas.height - 100) {
                        if (dashTimer > 0) {
                            if (!c.grazed) {
                                c.grazed = true;
                                triggerGraze(c, 'PERFECT DODGE!');
                            }
                            continue; // I-frames during dash shockwave
                        }"""

    if search_meteor in content:
        content = content.replace(search_meteor, replace_meteor)
    else:
         print(f"Error: search_meteor not found in {filepath}")

    with open(filepath, 'w') as f:
        f.write(content)

modify_file('index.html')
modify_file('chancla_bomb.html')
