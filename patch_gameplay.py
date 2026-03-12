import re

with open('index.html', 'r') as f:
    content = f.read()

# Update resetGame
old_resetGame = """            function resetGame() {
                player.x = canvas.width / 2;
                player.y = canvas.height - 70;
                player.lives = 3 + (gameData.upgrades.lives ? 1 : 0);
                player.shield = gameData.upgrades.shield;
                player.hitTimer = 0;
                isa.anger = isa.maxAnger;
                isa.x = canvas.width / 2;"""

new_resetGame = """            function resetGame() {
                player.x = canvas.width / 2;
                player.y = canvas.height - 70;
                player.lives = 3 + (gameData.upgrades.lives || 0);
                player.maxLives = 5 + (gameData.upgrades.lives || 0);
                player.shield = (gameData.upgrades.shield || 0) > 0;
                player.speed = 230 + (gameData.upgrades.speed || 0) * 15;
                player.hitTimer = 0;
                isa.anger = isa.maxAnger;
                isa.x = canvas.width / 2;"""

if old_resetGame in content:
    content = content.replace(old_resetGame, new_resetGame, 1)
    print("Success patch_resetGame")
else:
    print("Old block not found for resetGame!")

# Update trySlap
old_trySlap = """                if (slappedAny) {
                    slapCooldown = gameData.upgrades.cooldown ? 0.27 : 0.3;
                } else {
                    slapCooldown = 0.15;"""

new_trySlap = """                if (slappedAny) {
                    const cooldownReduction = (gameData.upgrades.cooldown || 0) * 0.015;
                    slapCooldown = Math.max(0.1, 0.3 - cooldownReduction);
                } else {
                    slapCooldown = 0.15;"""

if old_trySlap in content:
    content = content.replace(old_trySlap, new_trySlap, 1)
    print("Success patch_trySlap")
else:
    print("Old block not found for trySlap!")

with open('index.html', 'w') as f:
    f.write(content)
