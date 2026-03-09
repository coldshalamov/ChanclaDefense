import re

files = ['index.html', 'chancla_bomb.html']

for filepath in files:
    with open(filepath, 'r') as f:
        content = f.read()

    # Replace initialization
    content = content.replace(
        "let gameData = { coins: 0, upgrades: { lives: false, shield: false, cooldown: false }, bestScore: 0 };",
        "let gameData = { coins: 0, upgrades: { lives: 0, shield: 0, cooldown: 0, speed: 0 }, bestScore: 0 };"
    )

    # Replace fallback and add backward compatibility
    old_fallback = "if (!gameData.upgrades) gameData.upgrades = { lives: false, shield: false, cooldown: false };"
    new_fallback = """if (!gameData.upgrades) gameData.upgrades = { lives: 0, shield: 0, cooldown: 0, speed: 0 };
                // Backward compatibility for old boolean saves
                for (let key in gameData.upgrades) {
                    if (gameData.upgrades[key] === true) gameData.upgrades[key] = 1;
                    else if (gameData.upgrades[key] === false) gameData.upgrades[key] = 0;
                }
                if (gameData.upgrades.speed === undefined) gameData.upgrades.speed = 0;"""

    content = content.replace(old_fallback, new_fallback)

    with open(filepath, 'w') as f:
        f.write(content)

print("Patch applied.")
