import sys

def patch_file(filename):
    with open(filename, 'r') as f:
        content = f.read()

    # Patch player definition
    old_player = "const player = { x: canvas.width / 2, y: canvas.height - 70, w: 55, h: 45, speed: 230, lives: 3, maxLives: 5, shield: false, hitTimer: 0 };"
    new_player = "const player = { x: canvas.width / 2, y: canvas.height - 70, w: 55, h: 45, speed: 230, lives: 3, maxLives: 5, shield: false, hitTimer: 0, dashTimer: 0, dashCooldown: 0, dashDir: 0 };"

    if old_player in content:
        content = content.replace(old_player, new_player)
        print(f"Patched player in {filename}")
    else:
        print(f"Could not find old_player in {filename}")

    # Patch resetGame
    old_reset = """                player.shield = gameData.upgrades.shield;
                player.hitTimer = 0;"""
    new_reset = """                player.shield = gameData.upgrades.shield;
                player.hitTimer = 0;
                player.dashTimer = 0;
                player.dashCooldown = 0;
                player.dashDir = 0;"""

    if old_reset in content:
        content = content.replace(old_reset, new_reset)
        print(f"Patched resetGame in {filename}")
    else:
        print(f"Could not find old_reset in {filename}")

    with open(filename, 'w') as f:
        f.write(content)

patch_file('index.html')
patch_file('chancla_bomb.html')
