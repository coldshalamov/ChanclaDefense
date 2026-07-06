import sys

def replace_in_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    replacements = [
        (
            "                        // Add float text\n                        if (isPerfect) {\n                            gameData.coins += 2;\n                            gameData.stats.totalCoinsEarned += 2;\n                            addFloatText('PERFECT! +2💰' + comboText, c.x, c.y - 10);\n                            spawnImpact(c.x, c.y, true);\n                            playSound(850, 0.15);\n                            triggerShake(6, 0.2);\n                            triggerFlash(0.15, '#fff');\n                            hitStop = 0.15;\n                            spawnRoseExplosion(c.x, c.y);\n                        } else {\n                            gameData.coins += 1;\n                            gameData.stats.totalCoinsEarned += 1;\n                            addFloatText('SLAP! +1💰' + comboText, c.x, c.y);\n                            spawnImpact(c.x, c.y);\n                            playSound(600, 0.1);\n                        }",
            "                        // Add float text\n                        const pMultCoin = 1 + (gameData.prestige || 0) * 0.5;\n                        if (isPerfect) {\n                            gameData.coins += 2 * pMultCoin;\n                            gameData.stats.totalCoinsEarned += 2 * pMultCoin;\n                            addFloatText(`PERFECT! +${2 * pMultCoin}💰` + comboText, c.x, c.y - 10);\n                            spawnImpact(c.x, c.y, true);\n                            playSound(850, 0.15);\n                            triggerShake(6, 0.2);\n                            triggerFlash(0.15, '#fff');\n                            hitStop = 0.15;\n                            spawnRoseExplosion(c.x, c.y);\n                        } else {\n                            gameData.coins += 1 * pMultCoin;\n                            gameData.stats.totalCoinsEarned += 1 * pMultCoin;\n                            addFloatText(`SLAP! +${1 * pMultCoin}💰` + comboText, c.x, c.y);\n                            spawnImpact(c.x, c.y);\n                            playSound(600, 0.1);\n                        }"
        )
    ]

    # Try replacements
    for i, (search, replace) in enumerate(replacements):
        if search not in content:
            print(f"Warning: Match {i} not found in {filepath}!")
        else:
            content = content.replace(search, replace, 1)

    with open(filepath, 'w') as f:
        f.write(content)

    print(f"Successfully processed {filepath}")

replace_in_file('index.html')
replace_in_file('chancla_bomb.html')
