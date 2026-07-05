import re

files = ['index.html', 'chancla_bomb.html']

for filename in files:
    with open(filename, 'r') as f:
        content = f.read()

    # 11. MULTIPLIERS!
    content = content.replace('score += comboCount;', 'score += comboCount * (1 + (gameData.prestige || 0) * 0.5);')
    content = content.replace('score += 20 * c.rallyCount;', 'score += 20 * c.rallyCount * (1 + (gameData.prestige || 0) * 0.5);')
    content = content.replace('gameData.coins += 5 * c.rallyCount;', 'gameData.coins += Math.floor(5 * c.rallyCount * (1 + (gameData.prestige || 0) * 0.5));')
    content = content.replace('gameData.stats.totalCoinsEarned += 5 * c.rallyCount;', 'gameData.stats.totalCoinsEarned += Math.floor(5 * c.rallyCount * (1 + (gameData.prestige || 0) * 0.5));')
    content = content.replace('gameData.coins += 2;', 'gameData.coins += Math.floor(2 * (1 + (gameData.prestige || 0) * 0.5));')
    content = content.replace('gameData.stats.totalCoinsEarned += 2;', 'gameData.stats.totalCoinsEarned += Math.floor(2 * (1 + (gameData.prestige || 0) * 0.5));')
    content = content.replace('gameData.coins += 1;', 'gameData.coins += Math.floor(1 * (1 + (gameData.prestige || 0) * 0.5));')
    content = content.replace('gameData.stats.totalCoinsEarned += 1;', 'gameData.stats.totalCoinsEarned += Math.floor(1 * (1 + (gameData.prestige || 0) * 0.5));')
    content = content.replace('score += 5 + comboCount;', 'score += (5 + comboCount) * (1 + (gameData.prestige || 0) * 0.5);')
    content = content.replace('score += 5;', 'score += 5 * (1 + (gameData.prestige || 0) * 0.5);')
    content = content.replace('score += 1;', 'score += 1 * (1 + (gameData.prestige || 0) * 0.5);')
    content = content.replace('const bonus = 50 + (defeatedLevel - 1) * 50;', 'const bonus = Math.floor((50 + (defeatedLevel - 1) * 50) * (1 + (gameData.prestige || 0) * 0.5));')
    content = content.replace('score += dt * 50;', 'score += dt * 50 * (1 + (gameData.prestige || 0) * 0.5);')
    content = content.replace("ctx.fillText('Boss Bonus: +' + (50 + (gameData.stats.wins - 2) * 50) + ' 💰', canvas.width / 2, 270);", "ctx.fillText('Boss Bonus: +' + Math.floor((50 + (gameData.stats.wins - 2) * 50) * (1 + (gameData.prestige || 0) * 0.5)) + ' 💰', canvas.width / 2, 270);")

    with open(filename, 'w') as f:
        f.write(content)

print("Step 6 done")
