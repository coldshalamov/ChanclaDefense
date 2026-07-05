import os

def replace_in_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Replacements
    target1 = "let gameData = { coins: 0, upgrades: { lives: 0, shield: 0, cooldown: 0, speed: 0, power: 0 }, bestScore: 0, stats: { totalSlaps: 0, perfectSlaps: 0, gamesPlayed: 0, totalCoinsEarned: 0 }, achievements: {}, cosmetics: ['none'], currentHat: 'none' };"
    replacement1 = "let gameData = { coins: 0, upgrades: { lives: 0, shield: 0, cooldown: 0, speed: 0, power: 0 }, bestScore: 0, stats: { totalSlaps: 0, perfectSlaps: 0, gamesPlayed: 0, totalCoinsEarned: 0 }, achievements: {}, cosmetics: ['none'], currentHat: 'none', prestige: 0 };"

    target2 = "gameData = JSON.parse(saved);"
    replacement2 = "gameData = JSON.parse(saved);\n                    if (gameData.prestige === undefined) gameData.prestige = 0;"

    if target1 in content:
        content = content.replace(target1, replacement1)
    else:
        print(f"Failed to find target1 in {filepath}")

    if target2 in content:
        content = content.replace(target2, replacement2)
    else:
        print(f"Failed to find target2 in {filepath}")

    with open(filepath, 'w') as f:
        f.write(content)

replace_in_file("index.html")
replace_in_file("chancla_bomb.html")
