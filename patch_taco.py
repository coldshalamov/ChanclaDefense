import sys

def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # 1. Remove from applyPowerup
    apply_powerup_taco = """                if (p.kind === 'taco') {
                    // Taco Bomb clears all chanclas
                    if (chanclas.length > 0) {
                        for (let i = chanclas.length - 1; i >= 0; i--) {
                            const c = chanclas[i];
                            spawnImpact(c.x, c.y);
                            score += 5;
                            comboCount++;
                            chanclas.splice(i, 1);
                        }
                        shakeTimer = 0.5;
                        flash.timer = 0.2;
                        flash.color = '#ffffff';
                        playSound(200, 0.3);
                        addFloatText('TACO BOMB! 🌮💥', p.x, p.y);
                        sayRandom('super'); // reuse super dialogue or generic
                    } else {
                        addFloatText('🌮 (Mmm...)', p.x, p.y);
                        score += 5;
                    }
                }"""
    content = content.replace(apply_powerup_taco, "")

    # 2. Update updatePets
    update_pets_old = "const type = r < 0.2 ? 'phone' : (r < 0.45 ? 'taco' : 'beer');"
    update_pets_new = "const type = r < 0.2 ? 'phone' : 'beer';"
    content = content.replace(update_pets_old, update_pets_new)

    # 3. Remove from drawPowerups
    draw_powerups_taco = """                    } else if (p.kind === 'taco') {
                        ctx.font = '30px "Noto Color Emoji", "Apple Color Emoji", "Segoe UI Emoji", sans-serif';
                        ctx.textAlign = 'center';
                        ctx.textBaseline = 'middle';
                        ctx.fillText('🌮', 0, 0);"""
    content = content.replace(draw_powerups_taco, "")

    with open(filepath, 'w') as f:
        f.write(content)

patch_file('index.html')
patch_file('chancla_bomb.html')
