import re

files = ['index.html', 'chancla_bomb.html']

for filename in files:
    with open(filename, 'r') as f:
        content = f.read()

    # Score
    content = content.replace("score += comboCount;", "score += Math.floor(comboCount * getPrestigeMult());")
    content = content.replace("score += 20 * c.rallyCount;", "score += Math.floor(20 * c.rallyCount * getPrestigeMult());")
    content = content.replace("score += 5 + comboCount;", "score += Math.floor((5 + comboCount) * getPrestigeMult());")
    content = content.replace("score += 1;", "score += Math.floor(1 * getPrestigeMult());")
    content = content.replace("score += dt * 50;", "score += dt * 50 * getPrestigeMult();")

    # Coins
    content = content.replace("gameData.coins += 5 * c.rallyCount;", "gameData.coins += Math.floor(5 * c.rallyCount * getPrestigeMult());")
    content = content.replace("gameData.coins += 2;", "gameData.coins += Math.floor(2 * getPrestigeMult());")
    content = content.replace("gameData.coins += 1;", "gameData.coins += Math.floor(1 * getPrestigeMult());")
    content = content.replace("gameData.coins += bonus;", "gameData.coins += Math.floor(bonus * getPrestigeMult());")
    content = content.replace("gameData.coins += earned;", "gameData.coins += Math.floor(earned * getPrestigeMult());")

    # Total Coins Earned
    content = content.replace("gameData.stats.totalCoinsEarned += 5 * c.rallyCount;", "gameData.stats.totalCoinsEarned += Math.floor(5 * c.rallyCount * getPrestigeMult());")
    content = content.replace("gameData.stats.totalCoinsEarned += 2;", "gameData.stats.totalCoinsEarned += Math.floor(2 * getPrestigeMult());")
    content = content.replace("gameData.stats.totalCoinsEarned += 1;", "gameData.stats.totalCoinsEarned += Math.floor(1 * getPrestigeMult());")
    content = content.replace("gameData.stats.totalCoinsEarned += bonus;", "gameData.stats.totalCoinsEarned += Math.floor(bonus * getPrestigeMult());")
    content = content.replace("gameData.stats.totalCoinsEarned += earned;", "gameData.stats.totalCoinsEarned += Math.floor(earned * getPrestigeMult());")

    with open(filename, 'w') as f:
        f.write(content)
