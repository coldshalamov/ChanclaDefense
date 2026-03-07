import sys

def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # 1. Add dash properties to player object
    old_player = "const player = { x: canvas.width / 2, y: canvas.height - 70, w: 55, h: 45, speed: 230, lives: 3, maxLives: 5, shield: false, hitTimer: 0 };"
    new_player = "const player = { x: canvas.width / 2, y: canvas.height - 70, w: 55, h: 45, speed: 230, lives: 3, maxLives: 5, shield: false, hitTimer: 0, dashTimer: 0, dashCooldown: 0, dashDir: 0 };"
    if old_player in content:
        content = content.replace(old_player, new_player, 1)

    # 2. Add dash properties to resetGame
    old_reset = """                player.lives = 3 + (gameData.upgrades.lives ? 1 : 0);
                player.shield = gameData.upgrades.shield;
                player.hitTimer = 0;
"""
    new_reset = """                player.lives = 3 + (gameData.upgrades.lives ? 1 : 0);
                player.shield = gameData.upgrades.shield;
                player.hitTimer = 0;
                player.dashTimer = 0;
                player.dashCooldown = 0;
                player.dashDir = 0;
"""
    if old_reset in content:
        content = content.replace(old_reset, new_reset, 1)

    with open(filepath, 'w') as f:
        f.write(content)

patch_file('index.html')
patch_file('chancla_bomb.html')
print("Done")
