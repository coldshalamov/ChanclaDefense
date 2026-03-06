import os

files = ['index.html', 'chancla_bomb.html']

for file in files:
    with open(file, 'r') as f:
        content = f.read()

    # 1. Update player object
    old_player = "const player = { x: canvas.width / 2, y: canvas.height - 70, w: 55, h: 45, speed: 230, lives: 3, maxLives: 5, shield: false, hitTimer: 0 };"
    new_player = "const player = { x: canvas.width / 2, y: canvas.height - 70, w: 55, h: 45, speed: 230, lives: 3, maxLives: 5, shield: false, hitTimer: 0, dashTimer: 0, dashCooldown: 0, lastTapDir: null, lastTapTime: 0 };"
    content = content.replace(old_player, new_player)

    # 2. Update resetGame
    old_reset = """                player.lives = 3 + (gameData.upgrades.lives ? 1 : 0);
                player.shield = gameData.upgrades.shield;
                player.hitTimer = 0;
                isa.anger = isa.maxAnger;"""

    new_reset = """                player.lives = 3 + (gameData.upgrades.lives ? 1 : 0);
                player.shield = gameData.upgrades.shield;
                player.hitTimer = 0;
                player.dashTimer = 0;
                player.dashCooldown = 0;
                player.lastTapDir = null;
                player.lastTapTime = 0;
                isa.anger = isa.maxAnger;"""
    content = content.replace(old_reset, new_reset)

    # Update handleKey
    old_handle_key = """            function handleKey(e, isDown) {
                if (['ArrowLeft', 'a', 'A'].includes(e.key)) { keys.left = isDown; e.preventDefault(); }
                if (['ArrowRight', 'd', 'D'].includes(e.key)) { keys.right = isDown; e.preventDefault(); }"""

    new_handle_key = """            function handleKey(e, isDown) {
                if (['ArrowLeft', 'a', 'A'].includes(e.key)) {
                    if (isDown && !keys.left) {
                        const now = timeElapsed;
                        if (player.lastTapDir === 'left' && (now - player.lastTapTime) < 0.3 && player.dashCooldown <= 0) {
                            player.dashTimer = 0.25;
                            player.dashCooldown = 1.0;
                            playSound(600, 0.15); // optional sound for dash
                        }
                        player.lastTapDir = 'left';
                        player.lastTapTime = now;
                    }
                    keys.left = isDown;
                    e.preventDefault();
                }
                if (['ArrowRight', 'd', 'D'].includes(e.key)) {
                    if (isDown && !keys.right) {
                        const now = timeElapsed;
                        if (player.lastTapDir === 'right' && (now - player.lastTapTime) < 0.3 && player.dashCooldown <= 0) {
                            player.dashTimer = 0.25;
                            player.dashCooldown = 1.0;
                            playSound(600, 0.15);
                        }
                        player.lastTapDir = 'right';
                        player.lastTapTime = now;
                    }
                    keys.right = isDown;
                    e.preventDefault();
                }"""
    content = content.replace(old_handle_key, new_handle_key)

    # Update touch zones
    old_touch = """            function handleMobileZones(zone, dir) {
                zone.addEventListener('touchstart', (e) => {
                    if (state !== STATE.PLAYING) return;
                    touch[dir] = true;
                    e.preventDefault();
                }, { passive: false });"""

    new_touch = """            function handleMobileZones(zone, dir) {
                zone.addEventListener('touchstart', (e) => {
                    if (state !== STATE.PLAYING) return;
                    if (!touch[dir]) {
                        const now = timeElapsed;
                        if (player.lastTapDir === dir && (now - player.lastTapTime) < 0.3 && player.dashCooldown <= 0) {
                            player.dashTimer = 0.25;
                            player.dashCooldown = 1.0;
                            playSound(600, 0.15);
                        }
                        player.lastTapDir = dir;
                        player.lastTapTime = now;
                    }
                    touch[dir] = true;
                    e.preventDefault();
                }, { passive: false });"""
    content = content.replace(old_touch, new_touch)

    # Update speed calculation
    old_speed = """                const speed = player.speed;
                const moveLeft = keys.left || touch.left;
                const moveRight = keys.right || touch.right;"""

    new_speed = """                const speed = player.dashTimer > 0 ? player.speed * 2.5 : player.speed;
                if (player.dashTimer > 0 && Math.random() < 0.3) {
                    rosePetals.push({
                        x: player.x + (Math.random() - 0.5) * 20,
                        y: player.y + 10,
                        vy: 0,
                        vx: 0,
                        rotation: Math.random() * Math.PI * 2,
                        rotSpeed: (Math.random() - 0.5) * 2,
                        emoji: '💨',
                        size: 16 + Math.random() * 10
                    });
                }
                const moveLeft = keys.left || touch.left;
                const moveRight = keys.right || touch.right;"""
    content = content.replace(old_speed, new_speed)

    # Add timers
    old_timers = """                if (slapCooldown > 0) slapCooldown -= dt;
                if (slapEffect.timer > 0) slapEffect.timer -= dt;"""

    new_timers = """                if (slapCooldown > 0) slapCooldown -= dt;
                if (slapEffect.timer > 0) slapEffect.timer -= dt;
                if (player.dashTimer > 0) player.dashTimer -= dt;
                if (player.dashCooldown > 0) player.dashCooldown -= dt;"""
    content = content.replace(old_timers, new_timers)

    # Update collision check
    old_col = "if (!c.slapped && rectsOverlap(player, c)) {"
    new_col = "if (!c.slapped && rectsOverlap(player, c) && player.dashTimer <= 0) {"
    content = content.replace(old_col, new_col)

    # Update drawPlayer
    old_draw = """                drawPlayerAvatar(ctx, x, y, Math.min(w, h), specialAttackBar >= maxSpecialAttack, expression);
                if (player.shield) {"""

    new_draw = """                if (player.dashTimer > 0) ctx.globalAlpha = 0.5;
                drawPlayerAvatar(ctx, x, y, Math.min(w, h), specialAttackBar >= maxSpecialAttack, expression);
                if (player.dashTimer > 0) ctx.globalAlpha = 1.0;
                if (player.shield) {"""
    content = content.replace(old_draw, new_draw)

    with open(file, 'w') as f:
        f.write(content)

print("All patched")
