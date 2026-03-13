def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # 1. Update Isa collision damage
    old_isa = """                        if (distToIsa < 40 + c.w / 2) {
                            // Hit Isa
                            let damage = c.type === 'super' ? 15 : 8;
                            if (c.isPerfect) damage += 7;"""

    new_isa = """                        if (distToIsa < 40 + c.w / 2) {
                            // Hit Isa
                            let damage = c.type === 'super' ? 15 : (c.type === 'golden' ? 25 : 8);
                            if (c.isPerfect) damage += 7;"""

    content = content.replace(old_isa, new_isa, 1)

    # 2. Update player collision damage
    old_player = """                    if (!c.slapped && rectsOverlap(player, c)) {
                        if (player.shield) {
                            player.shield = false;
                            chanclas.splice(i, 1);
                            continue;
                        }
                        const dmg = c.type === 'super' ? 2 : 1;
                        comboCount = 0;
                        triggerShake(c.type === 'super' ? 15 : 8, 0.4);
                        player.lives -= dmg;"""

    new_player = """                    if (!c.slapped && rectsOverlap(player, c)) {
                        if (player.shield) {
                            player.shield = false;
                            chanclas.splice(i, 1);
                            continue;
                        }
                        const dmg = c.type === 'super' ? 2 : (c.type === 'golden' ? 2 : 1);
                        comboCount = 0;
                        triggerShake((c.type === 'super' || c.type === 'golden') ? 15 : 8, 0.4);
                        player.lives -= dmg;"""

    content = content.replace(old_player, new_player, 1)

    with open(filepath, 'w') as f:
        f.write(content)

patch_file('index.html')
patch_file('chancla_bomb.html')
