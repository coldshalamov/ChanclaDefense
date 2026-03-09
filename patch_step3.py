import sys

def patch_file(filename):
    with open(filename, 'r') as f:
        content = f.read()

    # Patch update player movement
    old_update = """                const speed = player.speed;
                const moveLeft = keys.left || touch.left;
                const moveRight = keys.right || touch.right;
                if (moveLeft) player.x -= speed * dt;
                if (moveRight) player.x += speed * dt;
                player.x = Math.max(player.w / 2 + 10, Math.min(canvas.width - player.w / 2 - 10, player.x));"""

    new_update = """                const speed = player.speed;
                if (player.dashTimer > 0) {
                    player.x += player.dashDir * speed * 2.5 * dt;
                } else {
                    const moveLeft = keys.left || touch.left;
                    const moveRight = keys.right || touch.right;
                    if (moveLeft) player.x -= speed * dt;
                    if (moveRight) player.x += speed * dt;
                }
                player.x = Math.max(player.w / 2 + 10, Math.min(canvas.width - player.w / 2 - 10, player.x));"""

    if old_update in content:
        content = content.replace(old_update, new_update)
        print(f"Patched update movement in {filename}")
    else:
        print(f"Could not find old_update in {filename}")

    # Patch update timers
    old_timers = """                if (slowEffect.timer > 0) slowEffect.timer -= dt;
                if (slapCooldown > 0) slapCooldown -= dt;
                if (slapEffect.timer > 0) slapEffect.timer -= dt;
                if (isa.hitTimer > 0) isa.hitTimer -= dt;
                if (player.hitTimer > 0) player.hitTimer -= dt;
                if (isa.chismeTimer > 0) isa.chismeTimer -= dt;"""

    new_timers = """                if (player.dashTimer > 0) {
                    player.dashTimer -= dt;
                    if (Math.random() < 0.2) {
                        rosePetals.push({
                            x: player.x + (Math.random() - 0.5) * 20,
                            y: player.y,
                            vy: -20,
                            rotation: Math.random() * Math.PI * 2,
                            rotSpeed: (Math.random() - 0.5) * 5,
                            emoji: '💨',
                            size: 24
                        });
                    }
                }
                if (player.dashCooldown > 0) player.dashCooldown -= dt;

                if (slowEffect.timer > 0) slowEffect.timer -= dt;
                if (slapCooldown > 0) slapCooldown -= dt;
                if (slapEffect.timer > 0) slapEffect.timer -= dt;
                if (isa.hitTimer > 0) isa.hitTimer -= dt;
                if (player.hitTimer > 0) player.hitTimer -= dt;
                if (isa.chismeTimer > 0) isa.chismeTimer -= dt;"""

    if old_timers in content:
        content = content.replace(old_timers, new_timers)
        print(f"Patched update timers in {filename}")
    else:
        print(f"Could not find old_timers in {filename}")


    # Patch drawPlayer
    old_draw_player = """                drawPlayerAvatar(ctx, x, y, Math.min(w, h), specialAttackBar >= maxSpecialAttack, expression);
                if (player.shield) {"""

    new_draw_player = """                if (player.dashTimer > 0) {
                    ctx.globalAlpha = 0.5;
                }
                drawPlayerAvatar(ctx, x, y, Math.min(w, h), specialAttackBar >= maxSpecialAttack, expression);
                ctx.globalAlpha = 1.0;
                if (player.shield) {"""

    if old_draw_player in content:
        content = content.replace(old_draw_player, new_draw_player)
        print(f"Patched drawPlayer in {filename}")
    else:
        print(f"Could not find old_draw_player in {filename}")

    with open(filename, 'w') as f:
        f.write(content)

patch_file('index.html')
patch_file('chancla_bomb.html')
