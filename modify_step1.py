import re

files = ['index.html', 'chancla_bomb.html']

for filename in files:
    with open(filename, 'r') as f:
        content = f.read()

    # 1. STATE enum
    content = content.replace("COSMETICS: 'cosmetics' };", "COSMETICS: 'cosmetics', PRESTIGE: 'prestige' };")

    # 2. gameData prestige property
    content = content.replace("cosmetics: ['none'], currentHat: 'none' };", "cosmetics: ['none'], currentHat: 'none', prestige: 0 };")

    # 3. gameData init in try catch
    content = content.replace("if (!gameData.currentHat) gameData.currentHat = 'none';", "if (!gameData.currentHat) gameData.currentHat = 'none';\n                if (gameData.prestige === undefined) gameData.prestige = 0;")

    with open(filename, 'w') as f:
        f.write(content)

print("Step 1 done")
