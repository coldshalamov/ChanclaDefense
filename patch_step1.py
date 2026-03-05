import re

with open('index.html', 'r') as f:
    content = f.read()

# Update player definition
content = content.replace(
    'const player = { x: canvas.width / 2, y: canvas.height - 70, w: 55, h: 45, speed: 230, lives: 3, maxLives: 5, shield: false, hitTimer: 0 };',
    'const player = { x: canvas.width / 2, y: canvas.height - 70, w: 55, h: 45, speed: 230, lives: 3, maxLives: 5, shield: false, hitTimer: 0, chiliTimer: 0 };'
)

# Update resetGame
content = content.replace(
    '''                player.shield = gameData.upgrades.shield;
                player.hitTimer = 0;''',
    '''                player.shield = gameData.upgrades.shield;
                player.hitTimer = 0;
                player.chiliTimer = 0;'''
)

with open('index.html', 'w') as f:
    f.write(content)
