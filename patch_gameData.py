import re

with open('index.html', 'r') as f:
    content = f.read()

old_block = """            let gameData = { coins: 0, upgrades: { lives: false, shield: false, cooldown: false }, bestScore: 0 };
            try {
                const saved = localStorage.getItem('chancla_bomb_save');
                if (saved) gameData = JSON.parse(saved);
                if (!gameData.upgrades) gameData.upgrades = { lives: false, shield: false, cooldown: false };
                if (gameData.coins === undefined) gameData.coins = 0;
                if (gameData.bestScore === undefined) gameData.bestScore = 0;
            } catch (e) { console.error(e); }"""

new_block = """            let gameData = { coins: 0, upgrades: { lives: 0, shield: 0, cooldown: 0, speed: 0 }, bestScore: 0 };
            try {
                const saved = localStorage.getItem('chancla_bomb_save');
                if (saved) gameData = JSON.parse(saved);
                if (!gameData.upgrades) gameData.upgrades = { lives: 0, shield: 0, cooldown: 0, speed: 0 };

                // Migrate old boolean saves to integer levels
                if (typeof gameData.upgrades.lives === 'boolean') gameData.upgrades.lives = gameData.upgrades.lives ? 1 : 0;
                if (typeof gameData.upgrades.shield === 'boolean') gameData.upgrades.shield = gameData.upgrades.shield ? 1 : 0;
                if (typeof gameData.upgrades.cooldown === 'boolean') gameData.upgrades.cooldown = gameData.upgrades.cooldown ? 1 : 0;

                // Initialize missing upgrades
                if (gameData.upgrades.speed === undefined) gameData.upgrades.speed = 0;
                if (gameData.coins === undefined) gameData.coins = 0;
                if (gameData.bestScore === undefined) gameData.bestScore = 0;
            } catch (e) { console.error(e); }"""

if old_block in content:
    content = content.replace(old_block, new_block, 1)
    with open('index.html', 'w') as f:
        f.write(content)
    print("Success")
else:
    print("Old block not found!")
