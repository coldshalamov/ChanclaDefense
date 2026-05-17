import re

def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # 1. Update chancla properties in spawn
    # Not strictly necessary to add rallyCount at spawn since undefined evaluates to falsy, but good practice.
    # Actually, let's just initialize it on parry.

    # 2. Update collision with Isa to add parry chance
    search_isa_collision = """                            if (c.isPerfect) {
                                addFloatText('CRITICAL! 💥', isa.x, isa.y + 30);
                                hitStop = 0.1;
                            }
                            addFloatText('REFLECTED! ↩️', isa.x, isa.y + 10);

                            playSound(900, 0.1); // Higher pitch for success
                            chanclas.splice(i, 1);

                            // Check win
                            if (isa.anger <= 0) {
                                state = STATE.WIN;
                                sayRandom('win');
                            }
                            continue;"""

    replace_isa_collision = """                            // Ping-Pong Rally (Dead Man's Volley) Mechanic
                            if (c.type !== 'meteor' && Math.random() < 0.3) {
                                // Isa parries the chancla back!
                                c.slapped = false;
                                c.rallyCount = (c.rallyCount || 0) + 1;
                                c.type = 'fire'; // Turns into a fire chancla
                                c.vy = baseSpeed + (c.rallyCount * 100);
                                c.vx = (player.x - c.x) * 2;

                                addFloatText('PARRY! 🏓', isa.x, isa.y + 30);
                                triggerFlash(0.2, '#ff0000');
                                playSound(1100, 0.15); // Parry sound
                            } else {
                                if (c.isPerfect) {
                                    addFloatText('CRITICAL! 💥', isa.x, isa.y + 30);
                                    hitStop = 0.1;
                                }
                                addFloatText('REFLECTED! ↩️', isa.x, isa.y + 10);

                                playSound(900, 0.1); // Higher pitch for success
                                chanclas.splice(i, 1);

                                // Check win
                                if (isa.anger <= 0) {
                                    state = STATE.WIN;
                                    sayRandom('win');
                                }
                            }
                            continue;"""

    if search_isa_collision in content:
        content = content.replace(search_isa_collision, replace_isa_collision)
        print(f"Patched Isa collision in {filepath}")
    else:
        print(f"Could not find Isa collision block in {filepath}")

    # 3. Update damage calculation in collision with Isa
    search_damage = """                            let damage = c.type === 'super' ? 15 : (c.type === 'fire' ? 12 : 8);
                            if (c.type === 'meteor') damage = 40;
                            if (c.isPerfect) damage += 7;"""

    replace_damage = """                            let damage = c.type === 'super' ? 15 : (c.type === 'fire' ? 12 : 8);
                            if (c.type === 'meteor') damage = 40;
                            if (c.isPerfect) damage += 7;
                            if (c.rallyCount > 0) damage += 10 * c.rallyCount;"""

    if search_damage in content:
        content = content.replace(search_damage, replace_damage)
        print(f"Patched damage calculation in {filepath}")
    else:
        print(f"Could not find damage calculation block in {filepath}")

    # 4. Update trySlap to handle MEGA HIT!
    search_try_slap = """                        // Increase special attack bar
                        specialAttackBar = Math.min(maxSpecialAttack, specialAttackBar + (isPerfect ? 25 : 15));"""

    replace_try_slap = """                        // Increase special attack bar
                        specialAttackBar = Math.min(maxSpecialAttack, specialAttackBar + (isPerfect ? 25 : 15));

                        // Check for Ping-Pong Rally
                        if (c.rallyCount > 0) {
                            addFloatText('MEGA HIT! 💥', c.x, c.y - 30);
                            triggerShake(10, 0.3);
                            triggerFlash(0.2, '#fff');
                            gameData.coins += 5 * c.rallyCount;
                            gameData.stats.totalCoinsEarned += 5 * c.rallyCount;
                            score += 20 * c.rallyCount;
                        }"""

    if search_try_slap in content:
        content = content.replace(search_try_slap, replace_try_slap)
        print(f"Patched trySlap in {filepath}")
    else:
        print(f"Could not find trySlap block in {filepath}")

    with open(filepath, 'w') as f:
        f.write(content)

patch_file('index.html')
patch_file('chancla_bomb.html')
