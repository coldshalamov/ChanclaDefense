import os

def replace_in_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Replacements
    replacements = [
        ("gameData.coins += 5 * c.rallyCount;", "gameData.coins += Math.floor((5 * c.rallyCount) * (1 + (gameData.prestige || 0) * 0.5));"),
        ("gameData.stats.totalCoinsEarned += 5 * c.rallyCount;", "gameData.stats.totalCoinsEarned += Math.floor((5 * c.rallyCount) * (1 + (gameData.prestige || 0) * 0.5));"),
        ("gameData.coins += 2;", "gameData.coins += Math.floor(2 * (1 + (gameData.prestige || 0) * 0.5));"),
        ("gameData.stats.totalCoinsEarned += 2;", "gameData.stats.totalCoinsEarned += Math.floor(2 * (1 + (gameData.prestige || 0) * 0.5));"),
        ("gameData.coins += 1;", "gameData.coins += Math.floor(1 * (1 + (gameData.prestige || 0) * 0.5));"),
        ("gameData.stats.totalCoinsEarned += 1;", "gameData.stats.totalCoinsEarned += Math.floor(1 * (1 + (gameData.prestige || 0) * 0.5));"),
        ("gameData.coins += bonus;", "gameData.coins += Math.floor(bonus * (1 + (gameData.prestige || 0) * 0.5));"),
        ("gameData.stats.totalCoinsEarned += bonus;", "gameData.stats.totalCoinsEarned += Math.floor(bonus * (1 + (gameData.prestige || 0) * 0.5));"),
        ("gameData.coins += earned;", "gameData.coins += Math.floor(earned * (1 + (gameData.prestige || 0) * 0.5));"),
        ("gameData.stats.totalCoinsEarned += earned;", "gameData.stats.totalCoinsEarned += Math.floor(earned * (1 + (gameData.prestige || 0) * 0.5));"),
        ("score += comboCount;", "score += Math.floor(comboCount * (1 + (gameData.prestige || 0) * 0.5));"),
        ("score += 20 * c.rallyCount;", "score += Math.floor((20 * c.rallyCount) * (1 + (gameData.prestige || 0) * 0.5));"),
        ("score += 5 + comboCount; // Bonus score for chaotic skill", "score += Math.floor((5 + comboCount) * (1 + (gameData.prestige || 0) * 0.5)); // Bonus score for chaotic skill"),
        ("score += 1;", "score += Math.floor(1 * (1 + (gameData.prestige || 0) * 0.5));"),
        ("score += dt * 50; // passive score", "score += (dt * 50) * (1 + (gameData.prestige || 0) * 0.5); // passive score")
    ]

    for target, replacement in replacements:
        if target in content:
            content = content.replace(target, replacement)
        else:
            print(f"Failed to find target in {filepath}: {target}")

    with open(filepath, 'w') as f:
        f.write(content)

replace_in_file("index.html")
replace_in_file("chancla_bomb.html")
