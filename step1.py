import re

files = ['index.html', 'chancla_bomb.html']

for filename in files:
    with open(filename, 'r') as f:
        content = f.read()

    # 1. Update STATE
    content = content.replace(
        "const STATE = { TITLE: 'title', PLAYING: 'playing', GAMEOVER: 'gameover', WIN: 'win', SHOP: 'shop', ACHIEVEMENTS: 'achievements', COSMETICS: 'cosmetics' };",
        "const STATE = { TITLE: 'title', PLAYING: 'playing', GAMEOVER: 'gameover', WIN: 'win', SHOP: 'shop', ACHIEVEMENTS: 'achievements', COSMETICS: 'cosmetics', PRESTIGE: 'prestige' };"
    )

    # 2. Update gameData initialization
    content = content.replace(
        "if (!gameData.currentHat) gameData.currentHat = 'none';",
        "if (!gameData.currentHat) gameData.currentHat = 'none';\n                if (gameData.prestige === undefined) gameData.prestige = 0;"
    )

    # 3. Add getPrestigeMult
    content = content.replace(
        "let hitStop = 0;",
        "let hitStop = 0;\n            function getPrestigeMult() { return 1 + (gameData.prestige || 0) * 0.5; }"
    )

    with open(filename, 'w') as f:
        f.write(content)
