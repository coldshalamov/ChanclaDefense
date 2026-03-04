import sys

def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # 1. Update gameData initialization
    old_gameData = "let gameData = { coins: 0, upgrades: { lives: false, shield: false, cooldown: false }, bestScore: 0 };"
    new_gameData = "let gameData = { coins: 0, upgrades: { lives: false, shield: false, cooldown: false }, bestScore: 0, stats: { totalSlaps: 0, perfectSlaps: 0, gamesPlayed: 0, totalCoinsEarned: 0 } };"
    content = content.replace(old_gameData, new_gameData, 1)

    old_gameData_fallback = "if (gameData.bestScore === undefined) gameData.bestScore = 0;"
    new_gameData_fallback = "if (gameData.bestScore === undefined) gameData.bestScore = 0;\n                if (!gameData.stats) gameData.stats = { totalSlaps: 0, perfectSlaps: 0, gamesPlayed: 0, totalCoinsEarned: 0 };"
    content = content.replace(old_gameData_fallback, new_gameData_fallback, 1)

    # 2. Update trySlap function
    old_trySlap_perfect = "gameData.coins += 2;\n                            addFloatText('PERFECT! +2💰' + comboText, c.x, c.y - 10);"
    new_trySlap_perfect = "gameData.coins += 2;\n                            gameData.stats.totalCoinsEarned += 2;\n                            gameData.stats.perfectSlaps += 1;\n                            gameData.stats.totalSlaps += 1;\n                            addFloatText('PERFECT! +2💰' + comboText, c.x, c.y - 10);"
    content = content.replace(old_trySlap_perfect, new_trySlap_perfect, 1)

    old_trySlap_normal = "gameData.coins += 1;\n                            addFloatText('SLAP! +1💰' + comboText, c.x, c.y);"
    new_trySlap_normal = "gameData.coins += 1;\n                            gameData.stats.totalCoinsEarned += 1;\n                            gameData.stats.totalSlaps += 1;\n                            addFloatText('SLAP! +1💰' + comboText, c.x, c.y);"
    content = content.replace(old_trySlap_normal, new_trySlap_normal, 1)

    # 3. Update endGame function
    old_endGame = "const earned = Math.floor(score / 10);\n                gameData.coins += earned;\n                gameData.bestScore = Math.max(gameData.bestScore, score);\n                saveGameData();"
    new_endGame = "const earned = Math.floor(score / 10);\n                gameData.coins += earned;\n                gameData.stats.totalCoinsEarned += earned;\n                gameData.stats.gamesPlayed += 1;\n                gameData.bestScore = Math.max(gameData.bestScore, score);\n                saveGameData();"
    content = content.replace(old_endGame, new_endGame, 1)

    # 4. Update updateChanclas win state
    old_win1 = "if (isa.anger <= 0) {\n                                state = STATE.WIN;\n                                sayRandom('win');\n                            }"
    new_win1 = "if (isa.anger <= 0) {\n                                state = STATE.WIN;\n                                gameData.stats.gamesPlayed += 1;\n                                const earned = Math.floor(score / 10);\n                                gameData.coins += earned;\n                                gameData.stats.totalCoinsEarned += earned;\n                                saveGameData();\n                                sayRandom('win');\n                            }"
    content = content.replace(old_win1, new_win1, 1)

    # 5. Update updateSpecialProjectiles win state
    old_win2 = "if (isa.anger <= 0) {\n                            state = STATE.WIN;\n                            sayRandom('win');\n                        }"
    new_win2 = "if (isa.anger <= 0) {\n                            state = STATE.WIN;\n                            gameData.stats.gamesPlayed += 1;\n                            const earned = Math.floor(score / 10);\n                            gameData.coins += earned;\n                            gameData.stats.totalCoinsEarned += earned;\n                            saveGameData();\n                            sayRandom('win');\n                        }"
    content = content.replace(old_win2, new_win2, 1)

    with open(filepath, 'w') as f:
        f.write(content)

patch_file('index.html')
patch_file('chancla_bomb.html')
print("Patched gameData successfully.")
