import re

files = ['index.html', 'chancla_bomb.html']

for filepath in files:
    with open(filepath, 'r') as f:
        content = f.read()

    # resetGame() lives
    content = content.replace(
        "player.lives = 3 + (gameData.upgrades.lives ? 1 : 0);",
        "player.lives = 3 + gameData.upgrades.lives;\n                player.maxLives = 5 + gameData.upgrades.lives;"
    )

    # resetGame() speed
    # add player speed reset after player.y
    content = content.replace(
        "player.y = canvas.height - 70;",
        "player.y = canvas.height - 70;\n                player.speed = 230 + (15 * gameData.upgrades.speed);"
    )

    # updateChanclas() shield block
    old_shield_hit = """                        if (player.shield) {
                            player.shield = false;"""
    new_shield_hit = """                        if (player.shield > 0) {
                            player.shield--;"""
    content = content.replace(old_shield_hit, new_shield_hit)

    # trySlap() cooldown
    content = content.replace(
        "slapCooldown = gameData.upgrades.cooldown ? 0.27 : 0.3;",
        "slapCooldown = Math.max(0.1, 0.3 - (0.03 * gameData.upgrades.cooldown));"
    )

    # drawPlayer() drawing shield
    old_shield_draw = """                if (player.shield) {
                    ctx.strokeStyle = '#9bfffa';
                    ctx.lineWidth = 3;
                    ctx.beginPath();
                    ctx.arc(x, y, w * 0.65, 0, Math.PI * 2);
                    ctx.stroke();
                }"""

    new_shield_draw = """                if (player.shield > 0) {
                    ctx.strokeStyle = '#9bfffa';
                    ctx.lineWidth = 3;
                    ctx.beginPath();
                    ctx.arc(x, y, w * 0.65, 0, Math.PI * 2);
                    ctx.stroke();
                    ctx.fillStyle = '#9bfffa';
                    ctx.font = '12px sans-serif';
                    ctx.textAlign = 'center';
                    ctx.fillText('🛡️x' + player.shield, x, y - h/2 - 25);
                }"""

    content = content.replace(old_shield_draw, new_shield_draw)

    with open(filepath, 'w') as f:
        f.write(content)

print("Patch applied.")
