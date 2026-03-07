import sys

def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    old_update_movement = """                const speed = player.speed;
                const moveLeft = keys.left || touch.left;
                const moveRight = keys.right || touch.right;
                if (moveLeft) player.x -= speed * dt;
                if (moveRight) player.x += speed * dt;
                player.x = Math.max(player.w / 2 + 10, Math.min(canvas.width - player.w / 2 - 10, player.x));"""

    new_update_movement = """                const speed = player.speed;
                const moveLeft = keys.left || touch.left;
                const moveRight = keys.right || touch.right;

                if (player.dashTimer > 0) {
                    player.x += player.dashDir * speed * 2.5 * dt;
                    player.dashTimer -= dt;
                    if (Math.random() < 0.3) {
                        rosePetals.push({
                            x: player.x + (Math.random() - 0.5) * 20,
                            y: player.y - 20,
                            vy: -50,
                            rotation: Math.random() * Math.PI * 2,
                            rotSpeed: (Math.random() - 0.5) * 5,
                            emoji: '💨',
                            size: 24
                        });
                    }
                } else {
                    if (moveLeft) player.x -= speed * dt;
                    if (moveRight) player.x += speed * dt;
                }
                if (player.dashCooldown > 0) player.dashCooldown -= dt;

                player.x = Math.max(player.w / 2 + 10, Math.min(canvas.width - player.w / 2 - 10, player.x));"""

    if old_update_movement in content:
        content = content.replace(old_update_movement, new_update_movement, 1)

    with open(filepath, 'w') as f:
        f.write(content)

patch_file('index.html')
patch_file('chancla_bomb.html')
print("Done")
